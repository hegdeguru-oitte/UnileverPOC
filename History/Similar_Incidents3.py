# """
# Enhanced Incident Analysis System
# --------------------------------
# This module provides a system for analyzing IT incidents by comparing them with historical cases
# and providing root cause analysis using LLM capabilities.

# Main Components:
# - ChromaDB for vector storage and similarity search
# - Groq LLM for incident analysis
# - Pandas for data handling

# Author: [Your Name]
# Date: November 2024
# """

# import os
# import pandas as pd
# import numpy as np
# from groq import Groq
# import chromadb
# from chromadb.utils import embedding_functions
# from chromadb.errors import InvalidCollectionException
# import logging
# from tqdm import tqdm

# # Configure logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)
# logging.getLogger('chromadb.telemetry.product.posthog').setLevel(logging.WARNING)

# class EnhancedIncidentAnalysisSystem:
#     """
#     A system for analyzing IT incidents and finding similar historical cases.
    
#     Attributes:
#         groq_client: Client for accessing Groq LLM API
#         chroma_client: Client for ChromaDB vector database
#         categories: Valid incident categories
#         collection: ChromaDB collection for storing incident embeddings
#     """
    
#     def __init__(self, groq_api_key, historical_incidents_file=None):
#         """
#         Initialize the incident analysis system.
        
#         Args:
#             groq_api_key (str): API key for Groq LLM service
#             historical_incidents_file (str, optional): Path to Excel file containing historical incidents
#         """
#         self.groq_client = Groq(api_key=groq_api_key)
#         self.chroma_client = chromadb.PersistentClient(path="./chroma_db")
#         self.embedding_function = embedding_functions.DefaultEmbeddingFunction()
#         self.categories = ["Software", "Hardware", "Network", "Security"]
        
#         # Initialize collection
#         try:
#             self.collection = self.chroma_client.get_collection(name="incident_embeddings")
#             logger.info("Loaded existing incident collection from ChromaDB")
#         except InvalidCollectionException:
#             self.collection = self.chroma_client.create_collection(
#                 name="incident_embeddings",
#                 embedding_function=self.embedding_function
#             )
#             logger.info("Created new incident collection in ChromaDB")
        
#         if historical_incidents_file:
#             self.load_historical_incidents(historical_incidents_file)

#     def load_historical_incidents(self, file_path):
#         """
#         Load historical incidents from Excel file into ChromaDB.
        
#         Args:
#             file_path (str): Path to Excel file containing historical incidents
            
#         Expected Excel columns:
#             - Incidents: Unique incident ID
#             - Description: Incident description
#             - Actions Taken: Resolution steps
#             - Participants: People involved
#             - Additional Info: Extra context
#         """
#         try:
#             df = pd.read_excel(file_path)
#             logger.info(f"Loading {len(df)} historical incidents into ChromaDB")
            
#             existing_count = self.collection.count()
#             if existing_count == 0:
#                 documents = df['Description'].tolist()
#                 ids = [str(id) for id in df['Incidents'].tolist()]
                
#                 # Prepare metadata with all required fields
#                 metadata = []
#                 for _, row in df.iterrows():
#                     metadata.append({
#                         'incident_id': str(row['Incidents']),
#                         'description': str(row['Description']),
#                         'actions_taken': str(row['Actions Taken']),
#                         'participants': str(row['Participants']),
#                         'additional_info': str(row.get('Additional Info', ''))
#                     })
                
#                 # Add to ChromaDB in batches
#                 batch_size = 100
#                 for i in tqdm(range(0, len(documents), batch_size)):
#                     batch_docs = documents[i:i + batch_size]
#                     batch_ids = ids[i:i + batch_size]
#                     batch_metadata = metadata[i:i + batch_size]
                    
#                     self.collection.add(
#                         documents=batch_docs,
#                         ids=batch_ids,
#                         metadatas=batch_metadata
#                     )
#                 logger.info(f"Successfully loaded {len(documents)} incidents into ChromaDB")
#             else:
#                 logger.info(f"Found {existing_count} existing incidents in ChromaDB")
                
#         except Exception as e:
#             logger.error(f"Error loading historical incidents: {str(e)}")
#             raise

#     def analyze_incident(self, incident_description, similarity_threshold=50, max_similar=2):
#         """
#         Analyze an incident and find similar historical cases.
        
#         Args:
#             incident_description (str): Description of the current incident
#             similarity_threshold (float): Minimum similarity score (0-100) to include in results
#             max_similar (int): Maximum number of similar incidents to return
            
#         Returns:
#             dict: Analysis results including root cause and similar incidents
#         """
#         try:
#             # Get root cause analysis
#             root_analysis = self.analyze_root_cause(incident_description)
            
#             # Find similar incidents using ChromaDB
#             similar_incidents = self.collection.query(
#                 query_texts=[incident_description],
#                 n_results=5  # Query more than needed to filter by similarity score
#             )
            
#             # Get detailed similarity analysis
#             if similar_incidents and len(similar_incidents['documents'][0]) > 0:
#                 historical_cases = similar_incidents['documents'][0]
#                 similarity_analysis = self.analyze_similarity(incident_description, historical_cases)
                
#                 # Filter and format results
#                 result = {
#                     'current_incident': {
#                         'description': incident_description,
#                         'analysis': root_analysis
#                     },
#                     'similar_incidents': []
#                 }
                
#                 # Process similar incidents
#                 processed_incidents = []
#                 for i, incident in enumerate(historical_cases):
#                     if i >= len(similarity_analysis):
#                         continue
                        
#                     similarity_score = similarity_analysis[i]['score']
#                     if similarity_score >= similarity_threshold:
#                         metadata = similar_incidents['metadatas'][0][i]
#                         incident_data = {
#                             'incident_id': metadata.get('incident_id', ''),
#                             'description': metadata.get('description', ''),
#                             'actions_taken': metadata.get('actions_taken', ''),
#                             'participants': metadata.get('participants', ''),
#                             'similarity_score': similarity_score
#                         }
#                         processed_incidents.append(incident_data)
                
#                 # Sort by similarity score and limit to max_similar
#                 processed_incidents.sort(key=lambda x: x['similarity_score'], reverse=True)
#                 result['similar_incidents'] = processed_incidents[:max_similar]
                
#                 return result
#             else:
#                 return {
#                     'current_incident': {
#                         'description': incident_description,
#                         'analysis': root_analysis
#                     },
#                     'similar_incidents': []
#                 }
                
#         except Exception as e:
#             logger.error(f"Error analyzing incident: {str(e)}")
#             raise

#     def analyze_root_cause(self, incident_description):
#         """
#         Analyze root cause using Groq LLM.
        
#         Args:
#             incident_description (str): Description of the incident
            
#         Returns:
#             dict: Structured analysis including category, root cause, impact, etc.
#         """
#         try:
#             prompt = f"""Analyze this IT incident with technical precision:

# Incident Description: {incident_description}

# Required Analysis Format:
# 1. Category: [MUST be exactly one of: Software, Hardware, Network, Security]
# 2. Root Cause: [Technical root cause analysis]
# 3. Impact Level: [Critical/High/Medium/Low]
# 4. Component: [Specific affected system/component]
# 5. Solution: [Technical resolution steps]
# 6. Prevention: [Technical preventive measures]

# Technical Analysis Guidelines:
# - Focus on underlying technical causes
# - Identify specific affected components
# - Consider system dependencies
# - Evaluate security implications
# - Look for configuration issues
# - Assess infrastructure impact
# - Consider application dependencies

# Use these Category Definitions:
# Software: Application, database, OS, code-related issues
# Hardware: Physical components, servers, storage, physical infrastructure
# Network: Connectivity, routing, DNS, bandwidth, network protocols
# Security: Access control, vulnerabilities, breaches, security policies

# Provide analysis in this exact format:
# CATEGORY: [exact category]
# ROOT_CAUSE: [detailed technical cause]
# IMPACT: [level]
# COMPONENT: [specific system]
# SOLUTION: [detailed steps]
# PREVENTION: [specific measures]"""

#             chat_completion = self.groq_client.chat.completions.create(
#                 messages=[{"role": "user", "content": prompt}],
#                 model="llama-3.1-8b-instant",
#                 temperature=0.1
#             )
            
#             response = chat_completion.choices[0].message.content.strip()
            
#             # Parse response
#             analysis = {}
#             current_key = None
#             current_value = []
            
#             for line in response.split('\n'):
#                 if line.strip():
#                     if any(line.startswith(f"{key}:") for key in ['CATEGORY', 'ROOT_CAUSE', 'IMPACT', 'COMPONENT', 'SOLUTION', 'PREVENTION']):
#                         if current_key:
#                             analysis[current_key] = ' '.join(current_value)
#                         current_key = line.split(':', 1)[0].strip()
#                         current_value = [line.split(':', 1)[1].strip()]
#                     else:
#                         if current_key:
#                             current_value.append(line.strip())
            
#             if current_key:
#                 analysis[current_key] = ' '.join(current_value)
            
#             # Validate category
#             if 'CATEGORY' in analysis:
#                 if analysis['CATEGORY'] not in self.categories:
#                     analysis['CATEGORY'] = 'Unknown'
            
#             return analysis
            
#         except Exception as e:
#             logger.error(f"Error in root cause analysis: {str(e)}")
#             return {
#                 'CATEGORY': 'Error',
#                 'ROOT_CAUSE': 'Analysis failed',
#                 'IMPACT': 'Unknown',
#                 'COMPONENT': 'Unknown',
#                 'SOLUTION': 'Analysis failed',
#                 'PREVENTION': 'Analysis failed'
#             }
       

#         pass

#     def analyze_similarity(self, current_incident, historical_incidents):
#         """
#         Analyze similarities between current and historical incidents.
        
#         Args:
#             current_incident (str): Description of current incident
#             historical_incidents (list): List of historical incident descriptions
            
#         Returns:
#             list: List of similarity analyses with scores and patterns
#         """
#         """Analyze similarities with optimized prompt and better error handling"""
#         try:
#             prompt = f"""Compare this incident with historical cases:

# Current Incident: {current_incident}

# Historical Cases:
# {chr(10).join(f"Case {i+1}: {case}" for i, case in enumerate(historical_incidents))}

# Analysis Requirements:
# 1. Technical similarity score (0-100)
# 2. Specific matching technical patterns
# 3. Shared root causes or components
# 4. Applicable historical solutions

# Compare these technical aspects:
# - Root cause patterns
# - Affected components
# - Technical symptoms
# - Resolution approaches
# - System dependencies

# For each case, provide analysis in this exact format:
# ID: [case number]
# SIMILARITY: [0-100]
# MATCH: [specific technical similarities]
# APPLICABLE_SOLUTION: [resolution steps]"""

#             chat_completion = self.groq_client.chat.completions.create(
#                 messages=[{"role": "user", "content": prompt}],
#                 model="llama-3.1-8b-instant",
#                 temperature=0.2
#             )
            
#             response = chat_completion.choices[0].message.content.strip()
            
#             # Improved parsing logic
#             similarities = []
#             current_case = {}
            
#             for line in response.split('\n'):
#                 line = line.strip()
#                 if not line:
#                     continue
                    
#                 if line.startswith('ID:'):
#                     if current_case and 'case' in current_case:
#                         similarities.append(current_case.copy())
#                     current_case = {'case': line.split(':', 1)[1].strip()}
#                 elif line.startswith('SIMILARITY:'):
#                     try:
#                         score = float(line.split(':', 1)[1].strip())
#                         current_case['score'] = min(max(score, 0), 100)
#                     except (ValueError, IndexError):
#                         current_case['score'] = 0
#                 elif line.startswith('MATCH:'):
#                     current_case['patterns'] = line.split(':', 1)[1].strip()
#                 elif line.startswith('APPLICABLE_SOLUTION:'):
#                     current_case['solution'] = line.split(':', 1)[1].strip()
            
#             # Add the last case if exists
#             if current_case and 'case' in current_case:
#                 similarities.append(current_case.copy())
            
#             # Validate and clean similarities
#             valid_similarities = []
#             required_keys = ['case', 'score', 'patterns', 'solution']
#             for sim in similarities:
#                 if all(k in sim for k in required_keys):
#                     valid_similarities.append(sim)
            
#             # Sort by score and return top 3
#             # return sorted(valid_similarities, key=lambda x: x.get('score', 0), reverse=True)[:3]
#             # Sort by score and return top 3 unique results
#             unique_similarities = []
#             unique_cases = set()
#             for sim in sorted(valid_similarities, key=lambda x: x.get('score', 0), reverse=True):
#                 case_id = sim.get('case')
#                 if case_id not in unique_cases:
#                     unique_similarities.append(sim)
#                     unique_cases.add(case_id)
#                     if len(unique_similarities) >= 3:  # Limit to top 3 results
#                         break

#             return unique_similarities

            
#         except Exception as e:
#             logger.error(f"Error in similarity analysis: {str(e)}")
#             return []
#         pass

# def main():
#     """
#     Main function to run the incident analysis system.
#     """
#     try:
#         # Get API key
#         groq_api_key = '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'
#         if not groq_api_key:
#             raise ValueError("GROQ_API_KEY environment variable is not set")
        
#         # Initialize system with historical incidents
#         historical_file = r'C:\Users\gurhegde\OneDrive - Deloitte (O365D)\CAI Playground\Pratik-Tasks\Unilever POC\Integration 1.2\History\Incidents_4X3.xlsx' #Change the input file here.
#         system = EnhancedIncidentAnalysisSystem(groq_api_key, historical_file)
        
#         # Get incident description from user
#         incident = input("Please describe the incident: ")
#         result = system.analyze_incident(incident)
        
#         # Print results
#         print("\nIncident Analysis:")
#         print("=================")
#         print("\nRoot Cause Analysis:")
#         for key, value in result['current_incident']['analysis'].items():
#             print(f"{key}: {value}")
        
#         print("\nSimilar Incidents:")
#         print("=================")
#         for i, similar in enumerate(result['similar_incidents'], 1):
#             print(f"\nIncident {i}:")
#             print(f"ID: {similar['incident_id']}")
#             print(f"Similarity Score: {similar['similarity_score']}%")
#             print(f"Description: {similar['description']}")
#             print(f"Actions Taken: {similar['actions_taken']}")
#             print(f"Participants: {similar['participants']}")
            
#     except Exception as e:
#         logger.error(f"Fatal error: {str(e)}")
#         raise

# if __name__ == "__main__":
#     main()






"""
Enhanced Incident Analysis System
--------------------------------
A comprehensive system for analyzing IT incidents by comparing them with historical cases
and providing root cause analysis using LLM capabilities.

Features:
- ChromaDB for vector storage and similarity search
- Groq LLM for incident analysis
- Multiple input methods for incidents
- Detailed incident comparison and analysis
"""

import os
import pandas as pd
import numpy as np
from groq import Groq
import chromadb
from chromadb.utils import embedding_functions
from chromadb.errors import InvalidCollectionException
import logging
from tqdm import tqdm
from config.settings import Settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logging.getLogger('chromadb.telemetry.product.posthog').setLevel(logging.WARNING)

class EnhancedIncidentAnalysisSystem:
    """
    A system for analyzing IT incidents and finding similar historical cases.
    """
    
    def __init__(self, groq_api_key=None, historical_incidents_file=None):
        """
        Initialize the incident analysis system.
        
        Args:
            groq_api_key (str, optional): API key for Groq LLM service
            historical_incidents_file (str, optional): Path to Excel file containing historical incidents
        """
        if groq_api_key is None:
            groq_api_key = Settings().GROQ_API_KEY
        self.groq_client = Groq(api_key=groq_api_key)
        self.chroma_client = chromadb.PersistentClient(path="./chroma_db")
        self.embedding_function = embedding_functions.DefaultEmbeddingFunction()
        self.categories = ["Software", "Hardware", "Network", "Security"]
        
        # Initialize collection
        try:
            self.collection = self.chroma_client.get_collection(name="incident_embeddings")
            logger.info("Loaded existing incident collection from ChromaDB")
        except InvalidCollectionException:
            self.collection = self.chroma_client.create_collection(
                name="incident_embeddings",
                embedding_function=self.embedding_function
            )
            logger.info("Created new incident collection in ChromaDB")
        
        if historical_incidents_file:
            self.load_historical_incidents(historical_incidents_file)

    def reset_database(self):
        """
        Delete all data from ChromaDB and reinitialize the collection.
        """
        try:
            # Delete the collection if it exists
            try:
                self.chroma_client.delete_collection("incident_embeddings")
                logger.info("Deleted existing collection")
            except:
                pass

            # Recreate the collection
            self.collection = self.chroma_client.create_collection(
                name="incident_embeddings",
                embedding_function=self.embedding_function
            )
            logger.info("Reinitialized ChromaDB collection")
            
            return True
        except Exception as e:
            logger.error(f"Error resetting database: {str(e)}")
            return False

    def delete_all_data(self):
        """
        Delete all ChromaDB data by removing the database directory.
        """
        try:
            # Close the client connection
            self.chroma_client.reset()
            
            # Remove the ChromaDB directory
            db_path = "./chroma_db"
            if os.path.exists(db_path):
                shutil.rmtree(db_path)
                logger.info("Successfully deleted ChromaDB directory")
            
            # Reinitialize the client and collection
            self.chroma_client = chromadb.PersistentClient(path="./chroma_db")
            self.collection = self.chroma_client.create_collection(
                name="incident_embeddings",
                embedding_function=self.embedding_function
            )
            logger.info("Reinitialized ChromaDB")
            
            return True
        except Exception as e:
            logger.error(f"Error deleting data: {str(e)}")
            return False

    def load_historical_incidents(self, file_path):
        """
        Load historical incidents from Excel file into ChromaDB.
        """
        try:
            df = pd.read_excel(file_path)
            logger.info(f"Loading {len(df)} historical incidents into ChromaDB")
            
            # Prepare data for ChromaDB
            documents = df['Description'].tolist()
            ids = [str(id) for id in df['Incidents'].tolist()]
            
            # Create metadata with explicit field mapping
            metadata = []
            for _, row in df.iterrows():
                metadata.append({
                    'incident_id': str(row['Incidents']),
                    'description': str(row['Description']),
                    'actions_taken': str(row['Actions Taken']),
                    'participants': str(row['Participants'])
                })
            
            # Add to ChromaDB in batches
            batch_size = 100
            for i in tqdm(range(0, len(documents), batch_size)):
                batch_docs = documents[i:i + batch_size]
                batch_ids = ids[i:i + batch_size]
                batch_metadata = metadata[i:i + batch_size]
                
                self.collection.add(
                    documents=batch_docs,
                    ids=batch_ids,
                    metadatas=batch_metadata
                )
            logger.info(f"Successfully loaded {len(documents)} incidents into ChromaDB")
                
        except Exception as e:
            logger.error(f"Error loading historical incidents: {str(e)}")
            raise

    def get_incident_input(self):
        """
        Get incident description from user with multiple input options.
        
        Returns:
            str: Incident description
        """
        print("\nChoose input method:")
        print("1. Single-line input")
        print("2. Multi-line input (Enter empty line to finish)")
        print("3. Load from text file")
        
        choice = input("\nEnter your choice (1-3): ").strip()
        
        if choice == "1":
            return input("\nPlease describe the incident: ").strip()
            
        elif choice == "2":
            print("\nEnter incident description (press Enter twice to finish):")
            lines = []
            while True:
                line = input()
                if line:
                    lines.append(line)
                elif lines:  # Empty line and we have content
                    break
            return "\n".join(lines)
            
        elif choice == "3":
            while True:
                file_path = input("\nEnter path to incident file: ").strip()
                if os.path.exists(file_path):
                    with open(file_path, 'r') as f:
                        return f.read().strip()
                else:
                    print("File not found. Please try again.")
        
        else:
            print("Invalid choice. Using single-line input.")
            return input("\nPlease describe the incident: ").strip()

    def analyze_incident(self, incident_description, similarity_threshold=50, max_similar=2):
        """
        Analyze an incident and find similar historical cases.
        """
        try:
            # Get root cause analysis
            root_analysis = self.analyze_root_cause(incident_description)
            
            # Find similar incidents using ChromaDB
            similar_incidents = self.collection.query(
                query_texts=[incident_description],
                n_results=5,  # Query more than needed to filter by similarity score
                include=['metadatas', 'documents', 'distances']
            )
            
            # Get detailed similarity analysis
            if similar_incidents and len(similar_incidents['documents'][0]) > 0:
                historical_cases = similar_incidents['documents'][0]
                similarity_analysis = self.analyze_similarity(incident_description, historical_cases)
                
                # Prepare results structure
                result = {
                    'current_incident': {
                        'description': incident_description,
                        'analysis': root_analysis
                    },
                    'similar_incidents': []
                }
                
                # Process similar incidents
                for i, (incident, metadata) in enumerate(zip(historical_cases, similar_incidents['metadatas'][0])):
                    if i >= len(similarity_analysis):
                        continue
                    
                    similarity_score = similarity_analysis[i]['score']
                    if similarity_score >= similarity_threshold:
                        incident_data = {
                            'incident_id': metadata.get('incident_id', ''),
                            'description': metadata.get('description', '').strip(),
                            'actions_taken': metadata.get('actions_taken', '').strip(),
                            'participants': metadata.get('participants', '').strip(),
                            'similarity_score': similarity_score
                        }
                        
                        # Only add if we have valid data
                        if any(incident_data.values()):
                            result['similar_incidents'].append(incident_data)
                
                # Sort by similarity score and limit to max_similar
                result['similar_incidents'] = sorted(
                    result['similar_incidents'],
                    key=lambda x: x['similarity_score'],
                    reverse=True
                )[:max_similar]
                
                return result
            else:
                return {
                    'current_incident': {
                        'description': incident_description,
                        'analysis': root_analysis
                    },
                    'similar_incidents': []
                }
                
        except Exception as e:
            logger.error(f"Error analyzing incident: {str(e)}")
            raise

    def analyze_root_cause(self, incident_description):
        """
        Analyze root cause using Groq LLM.
        """
        try:
            prompt = f"""Analyze this IT incident with technical precision:

Incident Description: {incident_description}

Required Analysis Format:
1. Category: [MUST be exactly one of: Software, Hardware, Network, Security]
2. Root Cause: [Technical root cause analysis]
3. Impact Level: [Critical/High/Medium/Low]
4. Component: [Specific affected system/component]
5. Solution: [Technical resolution steps]
6. Prevention: [Technical preventive measures]

Use these Category Definitions:
Software: Application, database, OS, code-related issues
Hardware: Physical components, servers, storage, physical infrastructure
Network: Connectivity, routing, DNS, bandwidth, network protocols
Security: Access control, vulnerabilities, breaches, security policies

Provide analysis in this exact format:
CATEGORY: [exact category]
ROOT_CAUSE: [detailed technical cause]
IMPACT: [level]
COMPONENT: [specific system]
SOLUTION: [detailed steps]
PREVENTION: [specific measures]"""

            chat_completion = self.groq_client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="llama-3.1-8b-instant",
                temperature=0.1
            )
            
            response = chat_completion.choices[0].message.content.strip()
            
            # Parse response
            analysis = {}
            current_key = None
            current_value = []
            
            for line in response.split('\n'):
                if line.strip():
                    if any(line.startswith(f"{key}:") for key in ['CATEGORY', 'ROOT_CAUSE', 'IMPACT', 'COMPONENT', 'SOLUTION', 'PREVENTION']):
                        if current_key:
                            analysis[current_key] = ' '.join(current_value)
                        current_key = line.split(':', 1)[0].strip()
                        current_value = [line.split(':', 1)[1].strip()]
                    else:
                        if current_key:
                            current_value.append(line.strip())
            
            if current_key:
                analysis[current_key] = ' '.join(current_value)
            
            # Validate category
            if 'CATEGORY' in analysis:
                if analysis['CATEGORY'] not in self.categories:
                    analysis['CATEGORY'] = 'Unknown'
            
            return analysis
            
        except Exception as e:
            logger.error(f"Error in root cause analysis: {str(e)}")
            return {
                'CATEGORY': 'Error',
                'ROOT_CAUSE': 'Analysis failed',
                'IMPACT': 'Unknown',
                'COMPONENT': 'Unknown',
                'SOLUTION': 'Analysis failed',
                'PREVENTION': 'Analysis failed'
            }

    def analyze_similarity(self, current_incident, historical_incidents):
        """
        Analyze similarities between current and historical incidents.
        """
        try:
            prompt = f"""Compare this incident with historical cases:

Current Incident: {current_incident}

Historical Cases:
{chr(10).join(f"Case {i+1}: {case}" for i, case in enumerate(historical_incidents))}

Compare these technical aspects:
- Root cause patterns
- Affected components
- Technical symptoms
- Resolution approaches
- System dependencies

For each case, provide analysis in this exact format:
ID: [case number]
SIMILARITY: [0-100]
MATCH: [specific technical similarities]
APPLICABLE_SOLUTION: [resolution steps]"""

            chat_completion = self.groq_client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="llama-3.1-8b-instant",
                temperature=0.2
            )
            
            response = chat_completion.choices[0].message.content.strip()
            
            # Parse response
            similarities = []
            current_case = {}
            
            for line in response.split('\n'):
                line = line.strip()
                if not line:
                    continue
                    
                if line.startswith('ID:'):
                    if current_case and 'case' in current_case:
                        similarities.append(current_case.copy())
                    current_case = {'case': line.split(':', 1)[1].strip()}
                elif line.startswith('SIMILARITY:'):
                    try:
                        score = float(line.split(':', 1)[1].strip())
                        current_case['score'] = min(max(score, 0), 100)
                    except (ValueError, IndexError):
                        current_case['score'] = 0
                elif line.startswith('MATCH:'):
                    current_case['patterns'] = line.split(':', 1)[1].strip()
                elif line.startswith('APPLICABLE_SOLUTION:'):
                    current_case['solution'] = line.split(':', 1)[1].strip()
            
            # Add the last case if exists
            if current_case and 'case' in current_case:
                similarities.append(current_case.copy())
            
            # Validate and clean similarities
            valid_similarities = []
            required_keys = ['case', 'score', 'patterns', 'solution']
            for sim in similarities:
                if all(k in sim for k in required_keys):
                    valid_similarities.append(sim)
            
            # Return unique top similarities
            unique_similarities = []
            seen_cases = set()
            for sim in sorted(valid_similarities, key=lambda x: x.get('score', 0), reverse=True):
                case_id = sim.get('case')
                if case_id not in seen_cases:
                    unique_similarities.append(sim)
                    seen_cases.add(case_id)
                    if len(unique_similarities) >= 3:
                        break
            
            return unique_similarities
            
        except Exception as e:
            logger.error(f"Error in similarity analysis: {str(e)}")
            return []


# Removed the main function and direct script execution logic
