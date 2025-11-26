import streamlit as st
import requests
import json
import base64
import time
from uuid import uuid4
import os # Import the os module for environment variables
#GEMINI_API_KEY
# --- Configuration and Constants ---
MODEL_NAME = "gemini-2.5-flash-preview-09-2025"
API_ENDPOINT = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL_NAME}:generateContent"

# --- Localization Dictionary ---
# Mapping UI strings for key Indian languages + English
UI_STRINGS = {
    "English": {
        "title": "Modular Plant Doctor AI Agent (6-Agent System)",
        "sidebar_config": "Configuration",
        "sidebar_language": "Select Output Language",
        "sidebar_history": "Session History (Mock VDB)",
        "input_header": "1. Input Data",
        "upload_plant": "Upload Plant Image (Mandatory)",
        "upload_soil": "Upload Soil Report (PDF File Only)",
        "no_soil_warning": "No soil report provided. Analysis will rely solely on the image.",
        "analyze_button": "🔬 Start 6-Agent Modular Analysis",
        "analysis_header": "2. AI Agent Analysis & Treatment Plan",
        "enter_key": "API Key not found. Please set the 'GEMINI_API_KEY' environment variable for deployment.",
        "upload_image": "Please upload a plant image to proceed.",
        "download_button": "⬇️ Download Analysis Report (Markdown)",
        "chat_header": "3. Ask Follow-up Questions (Chat Agent)",
        "chat_placeholder": "Ask a question about the diagnosis or treatment plan...",
        "chat_info": "The chat option will appear here after you successfully run the modular analysis (Step 2)."
    },
    "Hindi": {
        "title": "मॉड्यूलर प्लांट डॉक्टर एआई एजेंट (6-एजेंट सिस्टम)",
        "sidebar_config": "विन्यास (कॉन्फ़िगरेशन)",
        "sidebar_language": "आउटपुट भाषा चुनें",
        "sidebar_history": "सत्र इतिहास (मॉक VDB)",
        "input_header": "1. इनपुट डेटा",
        "upload_plant": "प्लांट इमेज अपलोड करें (अनिवार्य)",
        "upload_soil": "मिट्टी की रिपोर्ट अपलोड करें (केवल PDF फ़ाइल)",
        "no_soil_warning": "मिट्टी की कोई रिपोर्ट प्रदान नहीं की गई। विश्लेषण केवल छवि पर निर्भर करेगा।",
        "analyze_button": "🔬 6-एजेंट मॉड्यूलर विश्लेषण शुरू करें",
        "analysis_header": "2. एआई एजेंट विश्लेषण और उपचार योजना",
        "enter_key": "एपीआई कुंजी नहीं मिली। कृपया परिनियोजन (डिप्लॉयमेंट) के लिए 'GEMINI_API_KEY' वातावरण वैरिएबल सेट करें।",
        "upload_image": "आगे बढ़ने के लिए कृपया एक पौधा छवि अपलोड करें।",
        "download_button": "⬇️ विश्लेषण रिपोर्ट डाउनलोड करें (मार्कडाउन)",
        "chat_header": "3. फॉलो-अप प्रश्न पूछें (चैट एजेंट)",
        "chat_placeholder": "निदान या उपचार योजना के बारे में एक प्रश्न पूछें...",
        "chat_info": "चैट विकल्प यहां तभी दिखाई देगा जब आप मॉड्यूलर विश्लेषण (चरण 2) सफलतापूर्वक चला लेंगे।"
    },
    "Marathi": {
        "title": "मॉड्यूलर प्लांट डॉक्टर एआय एजंट (6-एजंट प्रणाली)",
        "sidebar_config": "कॉन्फिगरेशन",
        "sidebar_language": "आउटपुट भाषा निवडा",
        "sidebar_history": "सत्र इतिहास (मॉक VDB)",
        "input_header": "1. इनपुट डेटा",
        "upload_plant": "वनस्पतीची प्रतिमा अपलोड करा (अनिवार्य)",
        "upload_soil": "मातीचा अहवाल अपलोड करा (केवळ PDF फाईल)",
        "no_soil_warning": "मातीचा अहवाल दिलेला नाही. विश्लेषण केवळ प्रतिमेवर अवलंबून असेल.",
        "analyze_button": "🔬 6-एजंट मॉड्यूलर विश्लेषण सुरू करा",
        "analysis_header": "2. एआय एजंट विश्लेषण आणि उपचार योजना",
        "enter_key": "API की आढळली नाही. कृपया डिप्लॉयमेंटसाठी 'GEMINI_API_KEY' एन्व्हायरमेंट व्हेरिएबल सेट करा.",
        "upload_image": "पुढे जाण्यासाठी कृपया वनस्पतीची प्रतिमा अपलोड करा.",
        "download_button": "⬇️ विश्लेषण अहवाल डाउनलोड करा (मार्कडाउन)",
        "chat_header": "3. फॉलो-अप प्रश्न विचारा (चॅट एजंट)",
        "chat_placeholder": "निदान किंवा उपचार योजनेबद्दल प्रश्न विचारा...",
        "chat_info": "मॉड्यूलर विश्लेषण (पायरी 2) यशस्वीरित्या चालवल्यानंतर चॅट पर्याय येथे दिसेल."
    },
    # Add other Indian languages here if needed, or they will default to English if not defined.
    # For now, Hindi and Marathi provide a good demonstration.
}

# --- Session and Data Management (MOCK VDB/Access Management) ---

class PlantAgentSessionManager:
    """
    Simulates a Vector DB and Access Management using Streamlit's session state.
    Each session (user) gets a unique ID and its history is stored under that ID.
    This provides 'proper access management' in a single-file, session-based context.
    """
    def __init__(self):
        # Initialize session state variables if they don't exist
        if 'session_id' not in st.session_state:
            st.session_state['session_id'] = str(uuid4()) # Unique user/session ID
        if 'history' not in st.session_state:
            st.session_state['history'] = {}
        if 'analysis_complete' not in st.session_state:
            st.session_state['analysis_complete'] = False
        if 'final_report_content' not in st.session_state:
            st.session_state['final_report_content'] = ""
        # New: Chat history state
        if 'chat_history' not in st.session_state:
            st.session_state['chat_history'] = []
        # New: Language state
        if 'selected_language' not in st.session_state:
            st.session_state['selected_language'] = "English" # Default

    def get_session_id(self):
        return st.session_state['session_id']

    def save_analysis(self, prompt, analysis_text):
        """Saves a new analysis result to the current session's history."""
        session_id = self.get_session_id()
        if session_id not in st.session_state['history']:
            st.session_state['history'][session_id] = []

        st.session_state['history'][session_id].append({
            'timestamp': time.strftime("%Y-%m-%d %H:%M:%S"),
            'prompt': prompt,
            'analysis': analysis_text
        })

    def get_history(self):
        """Retrieves the analysis history for the current user (session)."""
        session_id = self.get_session_id()
        return st.session_state['history'].get(session_id, [])

# --- Core API Interaction Logic (Helper Function) ---

def _call_gemini_agent(api_key: str, contents: list, system_instruction: str, agent_name: str) -> str | None:
    """
    Generic function to handle the Gemini API call with retries and system instruction.
    """
    if not api_key:
        st.error(f"{agent_name} failed: API Key is missing.")
        return None

    url = f"{API_ENDPOINT}?key={api_key}"
    headers = {'Content-Type': 'application/json'}
    
    payload = {
        "contents": contents,
        "systemInstruction": {"parts": [{"text": system_instruction}]}
    }

    # Exponential backoff parameters
    max_retries = 5
    delay = 1

    for attempt in range(max_retries):
        try:
            response = requests.post(url, headers=headers, data=json.dumps(payload), timeout=60)
            response.raise_for_status()
            
            result = response.json()
            candidate = result.get('candidates', [{}])[0]
            
            if 'text' in candidate.get('content', {}).get('parts', [{}])[0]:
                return candidate['content']['parts'][0]['text']
            
            st.warning(f"Analysis failed in {agent_name}: No text generated (Possible safety block).")
            return None

        except requests.exceptions.RequestException as e:
            st.error(f"{agent_name} API Request Error (Attempt {attempt + 1}/{max_retries}): {e}")
            if attempt < max_retries - 1:
                time.sleep(delay)
                delay *= 2
            else:
                st.error(f"{agent_name} failed. Max retries reached.")
                return None
        except Exception as e:
            st.error(f"An unexpected error occurred in {agent_name}: {e}")
            return None
    return None

# --- Specialized Agent Functions (Parallel & Series) ---

def agent_visual_id(api_key, image_base64, output_language):
    """Agent 1: Parallel Path - Identifies the plant type and visual symptoms."""
    system_instruction = (
        "You are the Plant Visual Identification Agent. Analyze the image to identify the plant type "
        "and list all visual symptoms of disease or distress observed on the leaves/stem. "
        f"Output ONLY the plant name and a concise, numbered list of symptoms. The entire output MUST be in {output_language}."
    )
    contents = [
        {"role": "user", "parts": [
            {"text": "Identify the plant and describe visual symptoms."},
            {"inlineData": {"mimeType": "image/jpeg", "data": image_base64}}
        ]}
    ]
    return _call_gemini_agent(api_key, contents, system_instruction, "Visual ID Agent")

def agent_soil_analysis(api_key, soil_content_base64, mime_type, output_language):
    """Agent 2: Parallel Path - Interprets the soil report (text or PDF)."""
    if not soil_content_base64:
        # Note: This fallback text remains in English internally for the agent chain to process.
        return "Soil Analysis: No soil report provided."
        
    system_instruction = (
        "You are the Soil Analysis Agent. Analyze the provided document (or extracted text) for pH, nutrient deficiencies, or other environmental stresses. "
        "If the input is a document, first extract the relevant text. Output ONLY a brief, structured summary of findings and potential impacts on plant health. "
        f"The entire output MUST be in {output_language}."
    )
    
    # Prompt the model to analyze the content, regardless of whether it's raw text or a file
    text_prompt = "Analyze this soil report document and summarize findings:"
    
    contents = [
        {"role": "user", "parts": [
            {"text": text_prompt},
            {"inlineData": {"mimeType": mime_type, "data": soil_content_base64}}
        ]}
    ]
    return _call_gemini_agent(api_key, contents, system_instruction, "Soil Analysis Agent")

def agent_diagnostic(api_key, visual_output, soil_output, output_language):
    """Agent 3: Series/Merge - Merges visual and soil data to make a final diagnosis."""
    # Since visual_output and soil_output are already localized, we need to instruct the model to interpret them.
    # The markdown heading must also be localized.
    ui = UI_STRINGS.get(output_language, UI_STRINGS["English"])
    
    system_instruction = (
        "You are the Diagnostic Agent. Synthesize the visual symptoms and the soil analysis (which are provided in your output language) to determine the primary disease, deficiency, or health status. "
        "Output ONLY the final diagnosis, including the specific disease name and supporting evidence (visual + soil). "
        f"The output must start with a level 2 markdown heading '## 2. Disease Identification (or Health Status)'. The entire output MUST be in {output_language}."
    )
    
    merged_input = f"--- VISUAL SYMPTOMS ---\n{visual_output}\n\n--- SOIL ANALYSIS ---\n{soil_output}"
    contents = [
        {"role": "user", "parts": [
            {"text": "Based on the combined reports, provide a comprehensive final diagnosis:\n" + merged_input}
        ]}
    ]
    return _call_gemini_agent(api_key, contents, system_instruction, "Diagnostic Agent")

def agent_treatment(api_key, diagnosis_output, output_language):
    """Agent 4: Series - Creates a detailed, actionable treatment plan."""
    ui = UI_STRINGS.get(output_language, UI_STRINGS["English"])
    
    # MODIFIED SYSTEM INSTRUCTION TO PRIORITIZE SOIL AMENDMENTS
    system_instruction = (
        "You are the Treatment Plan Agent. Based on the provided diagnosis (which is already in the target language), generate a detailed, step-by-step treatment plan. "
        "If the diagnosis indicates nutrient deficiency or soil imbalance, those corrective actions MUST be listed first as the top priority. "
        "Include specific product types (e.g., copper fungicide, balanced NPK fertilizer) and application instructions. "
        "The output must start with a level 2 markdown heading '## 3. Treatment Plan (Detailed steps)'. "
        f"The entire output MUST be in {output_language}."
    )
    contents = [
        {"role": "user", "parts": [
            {"text": "Based on this diagnosis, create a detailed treatment plan:\n" + diagnosis_output}
        ]}
    ]
    return _call_gemini_agent(api_key, contents, system_instruction, "Treatment Agent")

def agent_recovery(api_key, treatment_plan_output, output_language):
    """Agent 5: Series - Provides long-term recovery and maintenance tips."""
    ui = UI_STRINGS.get(output_language, UI_STRINGS["English"])
    
    system_instruction = (
        "You are the Fast Recovery and Maintenance Agent. Based on the previous diagnosis and treatment plan (which is already in the target language), generate 3-5 clear, concise tips for fast recovery and long-term preventative care. "
        "The output must start with a level 2 markdown heading '## 4. Fast Recovery Tips (Maintenance advice)'. "
        f"The entire output MUST be in {output_language}."
    )
    contents = [
        {"role": "user", "parts": [
            {"text": "Generate long-term recovery tips and preventative maintenance advice for this case:\n" + treatment_plan_output}
        ]}
    ]
    return _call_gemini_agent(api_key, contents, system_instruction, "Recovery Agent")


def agent_chat(api_key, chat_query, report_context, output_language):
    """Agent 6: Post-Analysis Chat Agent."""
    system_instruction = (
        "You are the Plant Doctor Assistant. Your sole purpose is to answer follow-up questions from the user "
        "based *only* on the provided 'Analysis Report Context'. Do not use external knowledge. "
        f"Keep answers concise and conversational. The entire output MUST be in {output_language}."
    )

    contents = [
        {"role": "user", "parts": [
            {"text": f"Analysis Report Context:\n---\n{report_context}\n---\nUser Question: {chat_query}"}
        ]}
    ]
    return _call_gemini_agent(api_key, contents, system_instruction, "Chat Agent")

# --- Streamlit Application Layout ---

def handle_chat_input(manager, api_key):
    """Handles chat logic and updates history."""
    chat_query = st.session_state.chat_input
    if chat_query and api_key and st.session_state.final_report_content:
        # Append user message to history
        st.session_state.chat_history.append({"role": "user", "content": chat_query})
        
        # Call Chat Agent
        with st.spinner("Chat Agent thinking..."):
            # Pass selected language to the chat agent
            selected_language = st.session_state.get('selected_language', 'English')
            response_text = agent_chat(api_key, chat_query, st.session_state.final_report_content, selected_language)
        
        if response_text:
            st.session_state.chat_history.append({"role": "assistant", "content": response_text})
        else:
            st.session_state.chat_history.append({"role": "assistant", "content": "Sorry, I couldn't process that question based on the report."})
        
        # NOTE: st.chat_input automatically handles clearing its own value upon submission.

def main():
    st.set_page_config(
        page_title="Multi-Modal Plant Doctor AI",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Initialize the session manager
    manager = PlantAgentSessionManager()
    
    # --- API KEY HANDLING FOR DEPLOYMENT ---
    # Read API Key securely from environment variable
    api_key = os.environ.get("GEMINI_API_KEY")
    
    # Retrieve current UI strings based on selection
    selected_language = st.session_state.get('selected_language', 'English')
    ui = UI_STRINGS.get(selected_language, UI_STRINGS["English"])

    st.title(f"🌿 {ui['title']}")
    st.caption(f"Welcome, User ID: `{manager.get_session_id()}` (Access Key for your data)")
    
    # --- Sidebar for API Key, Language, and History ---
    with st.sidebar:
        st.header(ui['sidebar_config'])
        
        # Display environment variable status instead of input field
        if api_key:
            st.success("API Key loaded securely from environment variable.")
        else:
            # Display warning/error in the sidebar
            st.error("Deployment Warning: GEMINI_API_KEY environment variable not set.")

        # LANGUAGE SELECTION WIDGET
        languages = list(UI_STRINGS.keys()) # Use keys from the localization dictionary
        st.session_state['selected_language'] = st.selectbox(
            ui['sidebar_language'],
            languages,
            index=languages.index(selected_language) # Maintain state
        )
        selected_language = st.session_state['selected_language']
        # Re-fetch UI strings after language change (for the rest of the script run)
        ui = UI_STRINGS.get(selected_language, UI_STRINGS["English"])
        
        st.header(ui['sidebar_history'])
        history = manager.get_history()
        
        if history:
            st.write(f"Found {len(history)} previous analyses.")
            for i, record in enumerate(reversed(history)):
                with st.expander(f"Analysis {len(history) - i} ({record['timestamp'].split(' ')[1]})"):
                    st.caption(record['timestamp'])
                    st.code(record['prompt'][:100] + '...')
        else:
            st.info("No analysis history found for this session.")

    # --- Main Analysis Section ---

    st.header(ui['input_header'])

    col1, col2 = st.columns(2)

    with col1:
        plant_file = st.file_uploader(
            ui['upload_plant'],
            type=["jpg", "jpeg", "png"],
            help="Upload a clear image of the affected plant or leaves.",
            key="plant_image_uploader"
        )
        # Display uploaded image preview
        if plant_file is not None:
            st.image(plant_file, caption='Uploaded Plant Image', use_column_width='auto')

    with col2:
        soil_file = st.file_uploader(
            ui['upload_soil'],
            type=["pdf"],
            help="Upload a PDF soil report. The AI will extract and summarize the data.",
            key="soil_file_uploader"
        )
        soil_base64 = None
        soil_mime_type = None

        if soil_file is not None:
            # Read PDF bytes and convert to Base64
            soil_bytes = soil_file.getvalue()
            soil_base64 = base64.b64encode(soil_bytes).decode('utf-8')
            soil_mime_type = soil_file.type
            st.success(f"Soil report detected: {soil_file.name}")
        else:
            st.warning(ui['no_soil_warning'])

    analyze_button = st.button(ui['analyze_button'], type="primary", use_container_width=True)

    st.divider()

    # --- Orchestrator and Output Section ---
    st.header(ui['analysis_header'])

    if analyze_button:
        if not api_key:
            st.error(ui['enter_key']) # Error message for missing env var
            return
        if plant_file is None:
            st.error(ui['upload_image'])
            return

        image_bytes = plant_file.getvalue()
        image_base64 = base64.b64encode(image_bytes).decode('utf-8')
        
        # Reset the completion state and chat history at the start of a new analysis
        st.session_state.analysis_complete = False
        st.session_state.chat_history = []
        
        # Start Orchestration
        with st.spinner(f"Agent 1 & 2 (Parallel): Identifying Visual Symptoms and Analyzing Soil in {selected_language}..."):
            # Parallel Path 1 (Visual)
            visual_output = agent_visual_id(api_key, image_base64, selected_language)
            # Parallel Path 2 (Soil)
            # Pass Base64 content and mime type for PDF analysis
            soil_output = agent_soil_analysis(api_key, soil_base64, soil_mime_type, selected_language)
            
            if not visual_output:
                st.error("Visual ID Agent failed. Cannot continue diagnosis.")
                return

        # Agent 3: Series/Merge - Diagnostic Agent
        with st.spinner("Agent 3 (Series/Merge): Synthesizing data for final diagnosis..."):
            diagnosis_output = agent_diagnostic(api_key, visual_output, soil_output, selected_language)
            if not diagnosis_output:
                st.error("Diagnostic Agent failed. Cannot generate treatment plan.")
                return
        
        # Agent 4: Series - Treatment Agent
        with st.spinner("Agent 4 (Series): Generating detailed treatment plan..."):
            treatment_plan_output = agent_treatment(api_key, diagnosis_output, selected_language)
            if not treatment_plan_output:
                st.error("Treatment Agent failed. Cannot generate recovery tips.")
                return

        # Agent 5: Series - Recovery Agent
        with st.spinner("Agent 5 (Series): Generating fast recovery tips..."):
            recovery_tips_output = agent_recovery(api_key, treatment_plan_output, selected_language)
            if not recovery_tips_output:
                st.error("Recovery Agent failed. Showing partial results.")

        st.success(f"Modular Analysis Complete! Output Language: {selected_language}")
        
        # Assemble the final structured report
        final_report = f"""
# Plant Doctor AI Analysis Report
Generated: {time.strftime("%Y-%m-%d %H:%M:%S")}
User ID: {manager.get_session_id()}

---

## 1. Plant Type & Identification
{visual_output.splitlines()[0] if visual_output else 'N/A'}

---

{diagnosis_output}

{treatment_plan_output}

{recovery_tips_output or 'Could not retrieve recovery tips.'}

---

### Internal Agent Summary
**Soil Report Summary:** {soil_output}
"""
        
        # Update session state for display and download
        st.session_state.final_report_content = final_report
        st.session_state.analysis_complete = True

        # Save the combined analysis result to the mock VDB history
        manager.save_analysis(soil_file.name if soil_file else "Image only analysis", final_report)

        st.balloons()
        # Rerun is not strictly needed here, display and chat functionality should proceed below.

    # --- Display Final Report, Download, and Chat Interface ---

    if st.session_state.analysis_complete:
        st.markdown(st.session_state.final_report_content)
        
        st.download_button(
            label=ui['download_button'],
            data=st.session_state.final_report_content,
            file_name="plant_analysis_report.md",
            mime="text/markdown",
            use_container_width=True
        )

        st.divider()

        st.header(ui['chat_header'])

        # Display Chat History
        chat_container = st.container(height=300)
        with chat_container:
            for message in st.session_state.chat_history:
                avatar = "🤖" if message["role"] == "assistant" else "👤"
                with st.chat_message(message["role"], avatar=avatar):
                    st.markdown(message["content"])

        # Chat Input
        chat_input = st.chat_input(
            ui['chat_placeholder'],
            key="chat_input",
            on_submit=handle_chat_input,
            args=(manager, api_key)
        )
    else:
        st.info(ui['chat_info'])


if __name__ == "__main__":
    main()