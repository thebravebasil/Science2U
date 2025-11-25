# Science2U - K-12 Science Learning Agent

A comprehensive science learning agent built using Google's Agent Development Kit (ADK) that applies all concepts from the 5-Day AI Agents Intensive Course.

## Project Overview

Science2U is an intelligent tutoring agent designed for K-12 students that provides personalized science learning experiences across 10 different science topics. The agent uses advanced multi-agent architecture and implements cutting-edge AI agent concepts.

## Available Science Topics

1. **Chemistry** - Atomic structure, chemical bonds, reactions
2. **Environmental Science** - Ecosystems, climate change, sustainability  
3. **Biology** - Cell biology, genetics, evolution
4. **Physics** - Forces, energy, waves, thermodynamics
5. **Astronomy** - Planets, stars, galaxies, universe
6. **Earth Science** - Geology, meteorology, oceanography
7. **Elective Science Coursework** - Forensics, nanotechnology, biotechnology
8. **Engineering** - Design process, problem-solving, various engineering fields
9. **Forensic Analysis** - Crime scene investigation, evidence analysis
10. **Oceanography** - Marine biology, ocean currents, marine ecosystems

## Agent Architecture & Features

### Multi-Agent System Implementation
- **Sequential Agents** - Coordinated workflow for question generation → evaluation → document creation
- **Loop Agents** - Iterative question-answer cycles until mastery is achieved
- **Parallel Agents** - Concurrent processing of different learning tasks
- **Agent Tools** - Specialized sub-agents working as tools for the main coordinator

### Core Learning Workflow
1. **Topic Selection** - User selects from 10 science topics
2. **Question Generation** - AI generates 15 questions per topic with varying difficulty
3. **Interactive Assessment** - Student answers questions with immediate feedback
4. **Progress Tracking** - System tracks correct answers and learning progress
5. **Study Document Generation** - Creates personalized 5000-character study guide based on correct answers
6. **Reinforcement Testing** - Additional questions to test understanding
7. **Adaptive Learning** - System adapts to student's performance level

### Advanced ADK Features Applied

#### 1. **Custom Tools & Function Tools**
- `save_user_progress()` - Tracks learning progress across sessions
- `get_user_progress()` - Retrieves historical performance data
- `generate_questions()` - Creates topic-specific questions
- `check_answer()` - Intelligent answer validation with flexible matching
- `generate_study_document()` - Creates personalized study materials

#### 2. **Session Management & Memory**
- **InMemorySessionService** - Manages conversation state
- **InMemoryMemoryService** - Long-term knowledge retention
- **preload_memory** tool - Enables personalized learning experiences
- Session state management for progress tracking

#### 3. **Agent Observability**
- **LoggingPlugin** - Comprehensive logging for debugging and monitoring
- Detailed execution traces for performance analysis
- Error handling and recovery mechanisms

#### 4. **Context Engineering**
- Intelligent prompt design for educational interactions
- Context-aware question generation
- Adaptive difficulty based on student performance

## Getting Started

### Prerequisites
- Python 3.8+
- Google API Key (Gemini)

### Installation

1. **Clone or download the Science2U folder**

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Set up your API key:**
   - Edit the `.env` file
   - Replace `your_api_key_here` with your actual Google API key

4. **Run the agent:**
```bash
python science2u_agent.py
```

## Usage Example

```
🧪 Welcome to Science2U - Your K-12 Science Learning Companion! 🧪

Available Topics:
1. Chemistry
2. Environmental Science
3. Biology
4. Physics
5. Astronomy
6. Earth Science
7. Elective science coursework
8. Engineering
9. Forensic Analysis
10. Oceanography

💬 You: I want to learn about Chemistry

🤖 Science2U: Great choice! Chemistry is fascinating. Let's start with some questions to assess your current knowledge. I'll ask you 15 questions, and once you get 15 correct answers, I'll create a personalized study guide for you.

Question 1: What is the chemical formula for water?

💬 You: H2O

🤖 Science2U: Excellent! That's correct. Water is indeed H2O - two hydrogen atoms bonded to one oxygen atom.

[Session continues with adaptive questioning and learning...]
```

## Technical Architecture

### Agent Hierarchy
```
Science2UCoordinator (Main Agent)
├── QuestionGenerator (Specialized Agent)
├── AnswerEvaluator (Specialized Agent)  
├── DocumentGenerator (Specialized Agent)
├── ProgressTracker (Specialized Agent)
└── QuizLoop (Loop Agent)
    ├── QuestionPresenter
    ├── AnswerChecker
    └── ProgressEvaluator
```

## Educational Benefits

### For Students:
- **Personalized Learning** - Adapts to individual learning pace and style
- **Immediate Feedback** - Real-time assessment and correction
- **Comprehensive Coverage** - 10 different science topics with 150+ questions
- **Study Materials** - Auto-generated study guides based on performance
- **Progress Tracking** - Visual progress across different topics

### For Educators:
- **Assessment Tool** - Evaluate student understanding across topics
- **Curriculum Support** - Aligned with K-12 science standards
- **Progress Monitoring** - Track student learning over time
- **Adaptive Content** - Questions adjust to student level

## Customization Options

### Adding New Topics:
1. Add topic to `self.topics` list
2. Create question bank in `_initialize_question_banks()`
3. Add topic-specific information in `generate_study_document()`

### Modifying Question Difficulty:
- Questions are tagged with difficulty levels: "easy", "medium", "hard"
- Adjust the question selection algorithm in `generate_questions()`

### Extending Agent Capabilities:
- Add new specialized agents to the multi-agent system
- Implement additional tools for enhanced functionality
- Integrate external APIs for real-time science data

## Performance Features

- **Efficient Question Management** - Smart question selection and rotation
- **Memory Optimization** - Context compaction for long sessions
- **Error Recovery** - Graceful handling of API failures
- **Scalable Architecture** - Supports multiple concurrent users

## Development Notes

### Code Structure:
- **science2u_agent.py** - Main agent implementation
- **requirements.txt** - Python dependencies
- **.env** - Environment configuration
- **README.md** - Documentation

### Key Design Patterns:
- **Multi-Agent Coordination** - Specialized agents for different tasks
- **Tool-Based Architecture** - Modular functionality through tools
- **State Management** - Persistent learning progress
- **Observable Systems** - Comprehensive logging and monitoring

## Future Enhancements

- **Visual Learning** - Integration with image and diagram generation
- **Voice Interaction** - Speech-to-text and text-to-speech capabilities
- **Gamification** - Points, badges, and achievement systems
- **Collaborative Learning** - Multi-student sessions and competitions
- **Advanced Analytics** - Detailed learning analytics and insights
- **Mobile App** - Native mobile application for on-the-go learning

## License

This project is intended for educational purposes.

## Contributing

This is a project demonstrating the application of ADK concepts. Feel free to fork and extend for your own educational purposes!

---

**Built with ❤️ using Google's Agent Development Kit (ADK)**

*Applying concepts from: Multi-agent systems, Custom tools, Session management, Memory systems, Agent observability, and Production deployment patterns.*
