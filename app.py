import streamlit as st
import PyPDF2
from langchain_cohere import ChatCohere
from langchain_groq import ChatGroq
from langchain.schema import HumanMessage
from dotenv import load_dotenv

load_dotenv()
llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0, api_key="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")

def extract_text_from_pdf(pdf_file):
    """Extract text from the uploaded PDF file."""
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    full_text = ''
    for page in pdf_reader.pages:
        full_text += page.extract_text()
    return full_text

def get_plan(substrand, grade_standard_country="kenya"):
    prompt = '''Unit 1: Introduction to Fractions
Strand: Number and Operation
Content Standard: Extend knowledge of simple fractions to define and represent quantities, sizes, and structures (PNG Curriculum Standard 3.1.7).
1. Purpose

Introduce the concept of fractions as parts of a whole. Students will:

    Explore fractions as equal parts.
    Compare fraction sizes.
    Apply knowledge to real-world examples like sharing food or dividing objects.

Performance Standards:
Students will:

    Define simple fractions and represent them with diagrams or objects.
    Recognize and explain fraction sizes (e.g., 1/2 is larger than 1/4).
    Apply fractions to solve real-world problems (e.g., sharing items equally).

2. Objectives

By the end of the lesson, students will:

    Define fractions as parts of a whole.
    Represent fractions (denominators 2, 3, 4, and 6) using paper strips or diagrams.
    Compare fraction sizes using visual aids and inequality signs (<, >).
    Solve sharing problems using fractions.

3. Planning and Preparation

Materials:

    Paper strips for folding into fractions.
    Chalkboard/whiteboard for diagrams.
    Objects (e.g., sticks, coins) to represent fractions.
    Pre-drawn fraction bars and number lines.

Classroom Setup:

    Arrange desks in pairs for collaboration.
    Central table for group activities.

Timing:

    Introduction: 5 minutes
    Mini-Lesson: 10 minutes
    Guided Practice: 15 minutes
    Independent Practice: 10 minutes
    Assessment & Wrap-Up: 10 minutes

Anticipated Challenges:

    Difficulty visualizing fractions → Use multiple representations (paper strips, drawings).
    Confusion with numerator and denominator → Reinforce meanings with examples.

Differentiation:

    Simplify fractions (halves, thirds) for struggling students.
    Introduce comparisons with more complex fractions for advanced learners.

4. Prior Knowledge

Students Should Know:

    Basic division (e.g., splitting objects equally).
    Counting and number recognition.
    Concept of parts and wholes (e.g., dividing items into equal portions).

Evaluation of Prior Knowledge:

    Observation: Warm-up scenarios like "Share 6 bananas among 3 friends."
    Quick Questions:
        "What happens if you cut a pizza into 4 parts and eat 1?"
        "If you divide 12 sticks into 3 groups, how many are in each?"
    Hands-On Tasks: Use objects to demonstrate sharing.

5. Lesson Flow

Introduction (5 mins):

    Engage students with relatable questions: “Who has shared food with friends? How did you ensure fairness?”
    Introduce fractions using an example: "Cut an orange into 4 equal parts—each part is a fraction."

Mini-Lesson (10 mins):

    Define fractions as parts of a whole with diagrams.
    Demonstrate fractions (1/2, 1/3, 1/4) using paper strips.
    Introduce inequality signs (<, >) to compare fractions visually.

Guided Practice (15 mins):

    Group Activity:
        Fold paper strips into fractions (halves, thirds, quarters).
        Represent fractions on a number line.
        Compare sizes of fractions collaboratively.
    Teacher Feedback: Address misconceptions during group work.

Independent Practice (10 mins):

    Individual Task:
        Represent 3/6 and 1/2 using diagrams; determine if they’re equivalent.
        Compare fractions (e.g., 1/4 and 1/3) using inequality signs.

Assessment & Wrap-Up (10 mins):

    Quick Quiz:
        "Draw and label 2/3 as a diagram."
        "Compare 1/2 and 1/4: Which is larger?"
    Discussion: Where do we use fractions in daily life?
    Preview: Next lesson—adding fractions!

6. Extension/Enrichment (Optional)

    Advanced Activity: Explore fractions with larger denominators (e.g., 1/8, 1/10).
    Creative Task: Create a story about sharing using fractions and illustrate it.

7. Assessment Tools

Diagnostic:

    Observation Task: Ask students to equally share objects (e.g., “Share 8 counters among 4 groups”).
    Quick Quiz:
        "What’s larger: 1/2 or 1/3?"
        "How many parts make up a whole in thirds?"
    Pre-Test: Fold paper strips into halves/thirds and check their understanding.

Formative:

    Group Tasks: Assess fraction folding and comparison skills.
    Oral Questions: Ask questions during activities to gauge reasoning.
    Checkpoint Questions: Pose mid-lesson challenges (e.g., "Fold a strip into 6 parts and color 2—what fraction is colored?").

Summative:

    Drawing Task: Represent fractions visually and explain.
    Word Problems: Solve scenarios like "A watermelon is cut into 8 parts; you eat 3—what fraction is left?"
    Quiz: Label fractions on a number line, compare fractions, and solve multi-step problems.
    Performance-Based Task: Divide items into fractions and explain solutions.

Teacher Notes:

    Differentiate tasks for various skill levels.
    Provide immediate and structured feedback for improvement.'''
    return llm.stream(f"Create a lesson plan in detail for the students of {grade_standard_country} for the topic {substrand} with the help of the following example: {prompt}")

st.title("Lesson Plan Generator")
st.write("Upload a curriculum PDF file to extract substrands and generate lesson plans or directly input a topic and grade/standard/country to create a lesson plan.")

uploaded_file = st.file_uploader("Upload PDF Document", type="pdf")
if uploaded_file is not None:
    st.write("Extracting text from the uploaded PDF...")
    pdf_text = extract_text_from_pdf(uploaded_file)
    
    st.write("Extracting substrands...")
    prompt = f"Extract all the substrands from this text and return them as a comma-separated list: {pdf_text}"
    response = llm.invoke([HumanMessage(content=prompt)])
    substrands_text = response.content
    substrands_list = [substrand.strip() for substrand in substrands_text.split(",")]
    
    st.write("Substrands extracted successfully! Select a substrand to generate a lesson plan:")
    
    for substrand in substrands_list:
        if st.button(f"Generate for: {substrand}"):
            st.write(f"Generating lesson plan for: {substrand}")
            st.write_stream(get_plan(substrand))

st.write("Or manually input details to create a custom lesson plan:")
topic = st.text_input("Enter the topic (e.g., Fractions):", "")
grade_standard_country = st.text_input("Enter the grade/standard/country (e.g., Grade 5, Kenya):", "")

if st.button("Generate Custom Lesson Plan"):
    if topic and grade_standard_country:
        st.write(f"Generating lesson plan for topic: {topic}, Grade/Standard/Country: {grade_standard_country}")
        st.write_stream(get_plan(topic, grade_standard_country))
    else:
        st.error("Please fill in both the topic and grade/standard/country fields.")
