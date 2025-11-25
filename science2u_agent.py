"""
Science2U - K-12 Science Learning Agent
A comprehensive science learning agent that applies concepts from the 5-Day AI Course:
- Multi-agent systems (Sequential, Parallel, Loop agents)
- Custom tools and function tools
- Session management and memory
- Agent evaluation and observability
"""

import os
import random
import asyncio
from typing import Dict, List, Any
from dotenv import load_dotenv

from google.adk.agents import Agent, LlmAgent, SequentialAgent, LoopAgent
from google.adk.models.google_llm import Gemini
from google.adk.runners import InMemoryRunner
from google.adk.sessions import InMemorySessionService
from google.adk.memory import InMemoryMemoryService
from google.adk.tools import FunctionTool, AgentTool, load_memory, preload_memory
from google.adk.tools.tool_context import ToolContext
from google.adk.plugins.logging_plugin import LoggingPlugin
from google.genai import types

# Load environment variables
load_dotenv()

# Configuration
retry_config = types.HttpRetryOptions(
    attempts=5,
    exp_base=7,
    initial_delay=1,
    http_status_codes=[429, 500, 503, 504]
)

class Science2UAgent:
    """Main Science2U Agent class implementing multi-agent architecture"""
    
    def __init__(self):
        self.topics = [
            "Chemistry", "Environmental Science", "Biology", "Physics",
            "Astronomy", "Earth Science", "Elective science coursework",
            "Engineering", "Forensic Analysis", "Oceanography"
        ]
        
        # Initialize services
        self.session_service = InMemorySessionService()
        self.memory_service = InMemoryMemoryService()
        
        # Question banks for each topic
        self.question_banks = self._initialize_question_banks()
        
        # User progress tracking
        self.user_progress = {}
        
        # Initialize agents
        self._setup_agents()
        
    def _initialize_question_banks(self) -> Dict[str, List[Dict]]:
        """Initialize question banks for each science topic"""
        return {
            "Chemistry": [
                {"question": "What is the atomic number of Carbon?", "answer": "6", "difficulty": "easy"},
                {"question": "What is the chemical formula for water?", "answer": "H2O", "difficulty": "easy"},
                {"question": "What type of bond forms between sodium and chlorine?", "answer": "ionic bond", "difficulty": "medium"},
                {"question": "What is Avogadro's number?", "answer": "6.022 × 10²³", "difficulty": "hard"},
                {"question": "What is the pH of pure water?", "answer": "7", "difficulty": "easy"},
                {"question": "What is the most abundant gas in Earth's atmosphere?", "answer": "nitrogen", "difficulty": "easy"},
                {"question": "What is the process of a solid turning directly into a gas?", "answer": "sublimation", "difficulty": "medium"},
                {"question": "What is the molecular geometry of methane (CH4)?", "answer": "tetrahedral", "difficulty": "hard"},
                {"question": "What is the common name for sodium chloride?", "answer": "salt", "difficulty": "easy"},
                {"question": "What is the oxidation state of oxygen in most compounds?", "answer": "-2", "difficulty": "medium"},
                {"question": "What is the name of the reaction where an acid and base neutralize each other?", "answer": "neutralization", "difficulty": "medium"},
                {"question": "What is the electron configuration of carbon?", "answer": "1s² 2s² 2p²", "difficulty": "hard"},
                {"question": "What is the term for the energy required to remove an electron from an atom?", "answer": "ionization energy", "difficulty": "hard"},
                {"question": "What is the chemical symbol for gold?", "answer": "Au", "difficulty": "easy"},
                {"question": "What is the process where a liquid turns into a gas?", "answer": "evaporation", "difficulty": "easy"}
            ],
            "Biology": [
                {"question": "What is the powerhouse of the cell?", "answer": "mitochondria", "difficulty": "easy"},
                {"question": "What is the process by which plants make food?", "answer": "photosynthesis", "difficulty": "easy"},
                {"question": "What is DNA an acronym for?", "answer": "deoxyribonucleic acid", "difficulty": "medium"},
                {"question": "How many chambers does a human heart have?", "answer": "4", "difficulty": "easy"},
                {"question": "What is the largest organ in the human body?", "answer": "skin", "difficulty": "easy"},
                {"question": "What is the basic unit of heredity?", "answer": "gene", "difficulty": "medium"},
                {"question": "What is the process of cell division called?", "answer": "mitosis", "difficulty": "medium"},
                {"question": "What is the scientific name for humans?", "answer": "Homo sapiens", "difficulty": "medium"},
                {"question": "What is the green pigment in plants called?", "answer": "chlorophyll", "difficulty": "easy"},
                {"question": "What is the study of fungi called?", "answer": "mycology", "difficulty": "hard"},
                {"question": "What is the longest bone in the human body?", "answer": "femur", "difficulty": "medium"},
                {"question": "What is the process where organisms change over time?", "answer": "evolution", "difficulty": "medium"},
                {"question": "What is the term for animals that eat both plants and meat?", "answer": "omnivores", "difficulty": "easy"},
                {"question": "What is the double helix structure found in?", "answer": "DNA", "difficulty": "medium"},
                {"question": "What is the smallest unit of life?", "answer": "cell", "difficulty": "easy"}
            ],
            "Physics": [
                {"question": "What is the speed of light in vacuum?", "answer": "299,792,458 m/s", "difficulty": "medium"},
                {"question": "What is Newton's first law of motion?", "answer": "an object at rest stays at rest", "difficulty": "medium"},
                {"question": "What is the unit of force?", "answer": "Newton", "difficulty": "easy"},
                {"question": "What is the acceleration due to gravity on Earth?", "answer": "9.8 m/s²", "difficulty": "easy"},
                {"question": "What is the formula for kinetic energy?", "answer": "½mv²", "difficulty": "medium"},
                {"question": "What is the unit of electrical resistance?", "answer": "Ohm", "difficulty": "easy"},
                {"question": "What is the relationship between frequency and wavelength?", "answer": "inversely proportional", "difficulty": "medium"},
                {"question": "What is absolute zero in Celsius?", "answer": "-273.15°C", "difficulty": "hard"},
                {"question": "What is the unit of power?", "answer": "Watt", "difficulty": "easy"},
                {"question": "What is Ohm's law?", "answer": "V = IR", "difficulty": "medium"},
                {"question": "What is the speed of sound in air at room temperature?", "answer": "343 m/s", "difficulty": "medium"},
                {"question": "What is the unit of energy?", "answer": "Joule", "difficulty": "easy"},
                {"question": "What is the law of conservation of energy?", "answer": "energy cannot be created or destroyed", "difficulty": "medium"},
                {"question": "What is the unit of frequency?", "answer": "Hertz", "difficulty": "easy"},
                {"question": "What is Einstein's famous equation?", "answer": "E=mc²", "difficulty": "easy"}
            ],
            "Environmental Science": [
                {"question": "What is the greenhouse effect?", "answer": "trapping of heat in Earth's atmosphere", "difficulty": "medium"},
                {"question": "What is the ozone layer?", "answer": "protective layer in the stratosphere", "difficulty": "medium"},
                {"question": "What is biodiversity?", "answer": "variety of life in ecosystems", "difficulty": "easy"},
                {"question": "What is acid rain caused by?", "answer": "sulfur dioxide and nitrogen oxides", "difficulty": "medium"},
                {"question": "What is the main cause of global warming?", "answer": "greenhouse gas emissions", "difficulty": "easy"},
                {"question": "What is deforestation?", "answer": "clearing of forests", "difficulty": "easy"},
                {"question": "What is renewable energy?", "answer": "energy from naturally replenishing sources", "difficulty": "easy"},
                {"question": "What is the carbon cycle?", "answer": "movement of carbon through ecosystems", "difficulty": "medium"},
                {"question": "What is eutrophication?", "answer": "excessive nutrients in water bodies", "difficulty": "hard"},
                {"question": "What is sustainable development?", "answer": "meeting present needs without compromising future", "difficulty": "medium"},
                {"question": "What is the water cycle?", "answer": "continuous movement of water on Earth", "difficulty": "easy"},
                {"question": "What is pollution?", "answer": "contamination of environment", "difficulty": "easy"},
                {"question": "What is conservation?", "answer": "protection and preservation of natural resources", "difficulty": "easy"},
                {"question": "What is an ecosystem?", "answer": "community of living and non-living things", "difficulty": "easy"},
                {"question": "What is climate change?", "answer": "long-term changes in global climate patterns", "difficulty": "easy"}
            ],
            "Astronomy": [
                {"question": "What is the closest star to Earth?", "answer": "the Sun", "difficulty": "easy"},
                {"question": "How many planets are in our solar system?", "answer": "8", "difficulty": "easy"},
                {"question": "What is the largest planet in our solar system?", "answer": "Jupiter", "difficulty": "easy"},
                {"question": "What is a light-year?", "answer": "distance light travels in one year", "difficulty": "medium"},
                {"question": "What is the name of our galaxy?", "answer": "Milky Way", "difficulty": "easy"},
                {"question": "What is a black hole?", "answer": "region where gravity is so strong nothing can escape", "difficulty": "medium"},
                {"question": "What is the red planet?", "answer": "Mars", "difficulty": "easy"},
                {"question": "What is a supernova?", "answer": "explosive death of a massive star", "difficulty": "medium"},
                {"question": "What is the asteroid belt?", "answer": "region between Mars and Jupiter with asteroids", "difficulty": "medium"},
                {"question": "What is the hottest planet in our solar system?", "answer": "Venus", "difficulty": "medium"},
                {"question": "What is a nebula?", "answer": "cloud of gas and dust in space", "difficulty": "medium"},
                {"question": "What is the smallest planet in our solar system?", "answer": "Mercury", "difficulty": "easy"},
                {"question": "What is the Great Red Spot?", "answer": "giant storm on Jupiter", "difficulty": "hard"},
                {"question": "What is a comet?", "answer": "icy body that orbits the Sun", "difficulty": "easy"},
                {"question": "What is the Big Bang theory?", "answer": "theory about the origin of the universe", "difficulty": "medium"}
            ],
            "Earth Science": [
                {"question": "What are the three types of rocks?", "answer": "igneous, sedimentary, metamorphic", "difficulty": "medium"},
                {"question": "What causes earthquakes?", "answer": "movement of tectonic plates", "difficulty": "medium"},
                {"question": "What is the Earth's core made of?", "answer": "iron and nickel", "difficulty": "medium"},
                {"question": "What is the water cycle?", "answer": "continuous movement of water", "difficulty": "easy"},
                {"question": "What is erosion?", "answer": "wearing away of rock and soil", "difficulty": "easy"},
                {"question": "What is the Richter scale used for?", "answer": "measuring earthquake magnitude", "difficulty": "medium"},
                {"question": "What is a volcano?", "answer": "opening in Earth's crust where magma erupts", "difficulty": "easy"},
                {"question": "What is the hardest mineral?", "answer": "diamond", "difficulty": "easy"},
                {"question": "What is weathering?", "answer": "breakdown of rocks by natural processes", "difficulty": "easy"},
                {"question": "What is the Ring of Fire?", "answer": "area around Pacific Ocean with many volcanoes", "difficulty": "medium"},
                {"question": "What is a fossil?", "answer": "remains of ancient organisms", "difficulty": "easy"},
                {"question": "What is the mantle?", "answer": "layer between Earth's crust and core", "difficulty": "medium"},
                {"question": "What is continental drift?", "answer": "movement of continents over time", "difficulty": "medium"},
                {"question": "What is a glacier?", "answer": "large mass of ice that moves slowly", "difficulty": "easy"},
                {"question": "What is the atmosphere?", "answer": "layer of gases surrounding Earth", "difficulty": "easy"}
            ],
            "Elective science coursework": [
                {"question": "What is forensic science?", "answer": "application of science to legal matters", "difficulty": "medium"},
                {"question": "What is nanotechnology?", "answer": "manipulation of matter at atomic scale", "difficulty": "hard"},
                {"question": "What is biotechnology?", "answer": "use of living systems for technology", "difficulty": "medium"},
                {"question": "What is robotics?", "answer": "design and operation of robots", "difficulty": "easy"},
                {"question": "What is artificial intelligence?", "answer": "simulation of human intelligence in machines", "difficulty": "medium"},
                {"question": "What is genetic engineering?", "answer": "direct manipulation of genes", "difficulty": "medium"},
                {"question": "What is renewable energy?", "answer": "energy from naturally replenishing sources", "difficulty": "easy"},
                {"question": "What is 3D printing?", "answer": "additive manufacturing process", "difficulty": "easy"},
                {"question": "What is virtual reality?", "answer": "computer-generated simulation of environment", "difficulty": "easy"},
                {"question": "What is quantum computing?", "answer": "computing using quantum mechanical phenomena", "difficulty": "hard"},
                {"question": "What is bioinformatics?", "answer": "application of computing to biological data", "difficulty": "hard"},
                {"question": "What is materials science?", "answer": "study of properties and applications of materials", "difficulty": "medium"},
                {"question": "What is cybersecurity?", "answer": "protection of digital information", "difficulty": "easy"},
                {"question": "What is machine learning?", "answer": "algorithms that improve through experience", "difficulty": "medium"},
                {"question": "What is data science?", "answer": "extraction of knowledge from data", "difficulty": "medium"}
            ],
            "Engineering": [
                {"question": "What is the engineering design process?", "answer": "systematic approach to solving problems", "difficulty": "medium"},
                {"question": "What is mechanical engineering?", "answer": "design and manufacture of machines", "difficulty": "easy"},
                {"question": "What is civil engineering?", "answer": "design and construction of infrastructure", "difficulty": "easy"},
                {"question": "What is electrical engineering?", "answer": "design of electrical systems", "difficulty": "easy"},
                {"question": "What is a prototype?", "answer": "early model of a product", "difficulty": "easy"},
                {"question": "What is stress in engineering?", "answer": "force per unit area", "difficulty": "medium"},
                {"question": "What is a blueprint?", "answer": "detailed technical drawing", "difficulty": "easy"},
                {"question": "What is CAD?", "answer": "Computer-Aided Design", "difficulty": "easy"},
                {"question": "What is structural engineering?", "answer": "design of structures to support loads", "difficulty": "medium"},
                {"question": "What is aerospace engineering?", "answer": "design of aircraft and spacecraft", "difficulty": "medium"},
                {"question": "What is biomedical engineering?", "answer": "application of engineering to medicine", "difficulty": "medium"},
                {"question": "What is chemical engineering?", "answer": "application of chemistry to industrial processes", "difficulty": "medium"},
                {"question": "What is software engineering?", "answer": "systematic approach to software development", "difficulty": "medium"},
                {"question": "What is environmental engineering?", "answer": "application of engineering to environmental problems", "difficulty": "medium"},
                {"question": "What is quality control?", "answer": "process of ensuring products meet standards", "difficulty": "easy"}
            ],
            "Forensic Analysis": [
                {"question": "What is DNA fingerprinting?", "answer": "identification using DNA patterns", "difficulty": "medium"},
                {"question": "What is ballistics?", "answer": "study of projectiles and firearms", "difficulty": "medium"},
                {"question": "What is toxicology?", "answer": "study of poisons and their effects", "difficulty": "medium"},
                {"question": "What is fingerprint analysis?", "answer": "identification using fingerprint patterns", "difficulty": "easy"},
                {"question": "What is forensic pathology?", "answer": "investigation of deaths for legal purposes", "difficulty": "hard"},
                {"question": "What is trace evidence?", "answer": "small physical evidence at crime scenes", "difficulty": "medium"},
                {"question": "What is chromatography used for in forensics?", "answer": "separating and analyzing substances", "difficulty": "hard"},
                {"question": "What is forensic anthropology?", "answer": "identification of human remains", "difficulty": "medium"},
                {"question": "What is blood spatter analysis?", "answer": "interpretation of blood patterns", "difficulty": "medium"},
                {"question": "What is digital forensics?", "answer": "recovery of digital evidence", "difficulty": "medium"},
                {"question": "What is handwriting analysis?", "answer": "examination of handwriting characteristics", "difficulty": "medium"},
                {"question": "What is forensic entomology?", "answer": "use of insects in legal investigations", "difficulty": "hard"},
                {"question": "What is chain of custody?", "answer": "documentation of evidence handling", "difficulty": "medium"},
                {"question": "What is forensic psychology?", "answer": "application of psychology to legal matters", "difficulty": "medium"},
                {"question": "What is crime scene reconstruction?", "answer": "determining sequence of events at crime scene", "difficulty": "hard"}
            ],
            "Oceanography": [
                {"question": "What percentage of Earth is covered by oceans?", "answer": "71%", "difficulty": "easy"},
                {"question": "What is the deepest part of the ocean?", "answer": "Mariana Trench", "difficulty": "medium"},
                {"question": "What causes ocean tides?", "answer": "gravitational pull of moon and sun", "difficulty": "medium"},
                {"question": "What is a tsunami?", "answer": "large ocean wave caused by underwater disturbance", "difficulty": "medium"},
                {"question": "What is the Gulf Stream?", "answer": "warm ocean current in Atlantic", "difficulty": "medium"},
                {"question": "What is marine biology?", "answer": "study of ocean life", "difficulty": "easy"},
                {"question": "What is coral bleaching?", "answer": "loss of color in coral due to stress", "difficulty": "medium"},
                {"question": "What is the abyssal zone?", "answer": "deepest part of the ocean", "difficulty": "hard"},
                {"question": "What is plankton?", "answer": "small organisms that drift in water", "difficulty": "easy"},
                {"question": "What is the continental shelf?", "answer": "shallow underwater area near continents", "difficulty": "medium"},
                {"question": "What is bioluminescence?", "answer": "production of light by living organisms", "difficulty": "medium"},
                {"question": "What is ocean acidification?", "answer": "decrease in ocean pH due to CO2 absorption", "difficulty": "hard"},
                {"question": "What is a hydrothermal vent?", "answer": "underwater hot spring", "difficulty": "medium"},
                {"question": "What is the thermocline?", "answer": "layer where temperature changes rapidly", "difficulty": "hard"},
                {"question": "What is upwelling?", "answer": "rising of deep ocean water to surface", "difficulty": "hard"}
            ]
        }

    def save_user_progress(self, tool_context: ToolContext, topic: str, correct_answers: int, total_questions: int) -> Dict[str, Any]:
        """Save user progress for a topic"""
        tool_context.state[f"progress:{topic}"] = {
            "correct_answers": correct_answers,
            "total_questions": total_questions,
            "completion_percentage": (correct_answers / total_questions) * 100
        }
        return {"status": "success", "message": f"Progress saved for {topic}"}

    def get_user_progress(self, tool_context: ToolContext, topic: str = None) -> Dict[str, Any]:
        """Get user progress for a topic or all topics"""
        if topic:
            progress = tool_context.state.get(f"progress:{topic}", {})
            return {"status": "success", "progress": progress}
        else:
            all_progress = {}
            for key, value in tool_context.state.items():
                if key.startswith("progress:"):
                    topic_name = key.replace("progress:", "")
                    all_progress[topic_name] = value
            return {"status": "success", "all_progress": all_progress}

    def generate_questions(self, topic: str, count: int = 15) -> List[Dict]:
        """Generate questions for a specific topic"""
        if topic not in self.question_banks:
            return []
        
        questions = self.question_banks[topic].copy()
        random.shuffle(questions)
        return questions[:min(count, len(questions))]

    def check_answer(self, question: str, user_answer: str, correct_answer: str) -> bool:
        """Check if user answer is correct (case-insensitive, flexible matching)"""
        user_answer = user_answer.lower().strip()
        correct_answer = correct_answer.lower().strip()
        
        # Direct match
        if user_answer == correct_answer:
            return True
        
        # Check if user answer contains the correct answer
        if correct_answer in user_answer or user_answer in correct_answer:
            return True
        
        return False

    def generate_study_document(self, topic: str, correct_questions: List[Dict]) -> str:
        """Generate a study document based on correctly answered questions"""
        if not correct_questions:
            return f"No questions were answered correctly for {topic}. Please try again!"
        
        document = f"""
# {topic} Study Guide

Based on your correct answers, here's a comprehensive study guide:

## Key Concepts You've Mastered:

"""
        
        for i, q in enumerate(correct_questions[:10], 1):  # Limit to 10 questions for document length
            document += f"""
### {i}. {q['question']}
**Answer:** {q['answer']}
**Difficulty:** {q['difficulty']}

"""
        
        # Add topic-specific additional information
        topic_info = {
            "Chemistry": "Chemistry is the study of matter and its properties. Focus on understanding atomic structure, chemical bonds, and reactions.",
            "Biology": "Biology is the study of living organisms. Key areas include cell structure, genetics, evolution, and ecology.",
            "Physics": "Physics deals with matter, energy, and their interactions. Important concepts include forces, energy, waves, and thermodynamics.",
            "Environmental Science": "Environmental science studies the environment and solutions to environmental problems. Focus on ecosystems, pollution, and sustainability.",
            "Astronomy": "Astronomy is the study of celestial objects and space. Key topics include planets, stars, galaxies, and the universe's structure.",
            "Earth Science": "Earth science studies our planet's physical characteristics. Important areas include geology, meteorology, and oceanography.",
            "Engineering": "Engineering applies scientific principles to design and build solutions. Focus on the design process and problem-solving.",
            "Forensic Analysis": "Forensic science applies scientific methods to legal investigations. Key areas include evidence analysis and crime scene investigation.",
            "Oceanography": "Oceanography studies the oceans and marine life. Important topics include ocean currents, marine ecosystems, and ocean chemistry."
        }
        
        if topic in topic_info:
            document += f"\n## About {topic}:\n{topic_info[topic]}\n"
        
        document += f"\n## Study Tips:\n"
        document += f"- Review the concepts you got right and understand why they're correct\n"
        document += f"- Practice similar questions to reinforce your knowledge\n"
        document += f"- Connect these concepts to real-world applications\n"
        document += f"- Don't hesitate to ask for clarification on any topic\n"
        
        # Limit document to approximately 5000 characters
        if len(document) > 5000:
            document = document[:4900] + "\n\n[Document truncated to stay within character limit]"
        
        return document

    def _setup_agents(self):
        """Setup all the agents using multi-agent architecture"""
        
        # Question Generator Agent
        self.question_generator = LlmAgent(
            name="QuestionGenerator",
            model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
            instruction="""You are a question generator for K-12 science topics. 
            Generate educational questions appropriate for the given topic and difficulty level.
            Focus on fundamental concepts that students should understand.""",
            output_key="generated_questions"
        )
        
        # Answer Evaluator Agent
        self.answer_evaluator = LlmAgent(
            name="AnswerEvaluator", 
            model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
            instruction="""You are an answer evaluator. Compare student answers with correct answers.
            Be flexible with variations in wording but ensure the core concept is correct.
            Provide encouraging feedback.""",
            output_key="evaluation_result"
        )
        
        # Document Generator Agent
        self.document_generator = LlmAgent(
            name="DocumentGenerator",
            model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
            instruction="""You are a study guide generator. Create comprehensive but concise study materials
            based on the topics and questions the student answered correctly. 
            Keep the document under 5000 characters and make it educational and engaging.""",
            output_key="study_document"
        )
        
        # Progress Tracker Agent
        self.progress_tracker = LlmAgent(
            name="ProgressTracker",
            model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
            instruction="""You track student progress and provide motivational feedback.
            Analyze performance and suggest areas for improvement.""",
            tools=[
                FunctionTool(self.save_user_progress),
                FunctionTool(self.get_user_progress)
            ],
            output_key="progress_update"
        )
        
        # Main Coordinator Agent
        self.coordinator = LlmAgent(
            name="Science2UCoordinator",
            model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
            instruction=f"""You are Science2U, a friendly K-12 science learning assistant.

Available topics: {', '.join(self.topics)}

Your workflow:
1. Help users select a science topic from the available list
2. Generate 15 questions on the selected topic
3. Collect answers and evaluate them
4. Once 15 correct answers are achieved, generate a study document
5. Generate additional questions to test understanding
6. Track progress and provide encouragement

Be encouraging, educational, and adapt to the student's level.
Always maintain a positive learning environment.""",
            tools=[
                AgentTool(agent=self.question_generator),
                AgentTool(agent=self.answer_evaluator), 
                AgentTool(agent=self.document_generator),
                AgentTool(agent=self.progress_tracker),
                preload_memory  # Enable memory for personalized learning
            ]
        )

    async def run_learning_session(self, user_id: str = "student", session_id: str = "learning_session"):
        """Run an interactive learning session"""
        
        # Setup runner with all services
        runner = InMemoryRunner(
            agent=self.coordinator,
            plugins=[LoggingPlugin()]  # Add observability
        )
        
        print("🧪 Welcome to Science2U - Your K-12 Science Learning Companion! 🧪")
        print("\nAvailable Topics:")
        for i, topic in enumerate(self.topics, 1):
            print(f"{i}. {topic}")
        
        while True:
            try:
                user_input = input("\n💬 You: ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'bye']:
                    print("👋 Thanks for learning with Science2U! Keep exploring science!")
                    break
                
                if not user_input:
                    continue
                
                # Create message content
                message = types.Content(
                    role="user", 
                    parts=[types.Part(text=user_input)]
                )
                
                print("🤖 Science2U: ", end="", flush=True)
                
                # Stream response
                async for event in runner.run_async(
                    user_id=user_id,
                    session_id=session_id, 
                    new_message=message
                ):
                    if event.is_final_response() and event.content and event.content.parts:
                        response_text = event.content.parts[0].text
                        if response_text and response_text != "None":
                            print(response_text)
                            break
                            
            except KeyboardInterrupt:
                print("\n👋 Session ended. Thanks for learning with Science2U!")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}")
                print("Let's try again!")

class QuizSession:
    """Handles quiz sessions with loop agent for iterative learning"""
    
    def __init__(self, science_agent: Science2UAgent, topic: str):
        self.science_agent = science_agent
        self.topic = topic
        self.questions = science_agent.generate_questions(topic, 15)
        self.current_question_index = 0
        self.correct_answers = []
        self.incorrect_answers = []
        
        # Quiz Loop Agent for iterative question-answer cycles
        self.quiz_loop = self._create_quiz_loop()
    
    def _create_quiz_loop(self):
        """Create a loop agent for quiz iterations"""
        
        # Question Presenter Agent
        question_presenter = LlmAgent(
            name="QuestionPresenter",
            model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
            instruction=f"""Present questions for {self.topic} in an engaging way.
            Ask one question at a time and wait for the student's answer.
            Be encouraging and educational.""",
            output_key="current_question"
        )
        
        # Answer Checker Agent  
        answer_checker = LlmAgent(
            name="AnswerChecker",
            model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
            instruction="""Check if the student's answer is correct.
            Provide immediate feedback - praise correct answers and gently correct wrong ones.
            Give hints for improvement when needed.""",
            output_key="answer_feedback"
        )
        
        # Progress Evaluator Agent
        progress_evaluator = LlmAgent(
            name="ProgressEvaluator", 
            model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
            instruction="""Evaluate if the student has answered enough questions correctly (15 correct answers).
            If yes, signal to exit the loop. If no, continue with more questions.""",
            tools=[FunctionTool(self._check_completion)],
            output_key="progress_status"
        )
        
        # Create Loop Agent
        return LoopAgent(
            name="QuizLoop",
            sub_agents=[question_presenter, answer_checker, progress_evaluator],
            max_iterations=50  # Prevent infinite loops
        )
    
    def _check_completion(self) -> Dict[str, Any]:
        """Check if quiz is complete (15 correct answers)"""
        if len(self.correct_answers) >= 15:
            return {"status": "complete", "exit_loop": True}
        else:
            return {"status": "continue", "correct_count": len(self.correct_answers)}

async def main():
    """Main function to run Science2U agent"""
    
    # Check for API key
    if not os.getenv("GOOGLE_API_KEY"):
        print("❌ Please set your GOOGLE_API_KEY in the .env file")
        return
    
    # Initialize Science2U Agent
    science_agent = Science2UAgent()
    
    # Run interactive learning session
    await science_agent.run_learning_session()

if __name__ == "__main__":
    asyncio.run(main())