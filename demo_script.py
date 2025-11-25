"""
Science2U Demo Script
Demonstrates the key features and capabilities of the Science2U agent
"""

import asyncio
import os
from dotenv import load_dotenv
from science2u_agent import Science2UAgent

async def demo_science2u():
    """Demonstrate Science2U capabilities"""
    
    print("🧪 Science2U Agent Demo 🧪")
    print("=" * 50)
    
    # Initialize the agent
    science_agent = Science2UAgent()
    
    print("\n1. 📚 Available Science Topics:")
    for i, topic in enumerate(science_agent.topics, 1):
        print(f"   {i}. {topic}")
    
    print("\n2. 🎯 Question Generation Demo:")
    chemistry_questions = science_agent.generate_questions("Chemistry", 5)
    print(f"   Generated {len(chemistry_questions)} Chemistry questions:")
    for i, q in enumerate(chemistry_questions, 1):
        print(f"   Q{i}: {q['question']} (Difficulty: {q['difficulty']})")
    
    print("\n3. ✅ Answer Checking Demo:")
    test_cases = [
        ("What is the chemical formula for water?", "H2O", "H2O"),
        ("What is the atomic number of Carbon?", "6", "6"),
        ("What is the pH of pure water?", "seven", "7")
    ]
    
    for question, user_answer, correct_answer in test_cases:
        is_correct = science_agent.check_answer(question, user_answer, correct_answer)
        status = "✅ Correct" if is_correct else "❌ Incorrect"
        print(f"   Q: {question}")
        print(f"   Student Answer: '{user_answer}' | Correct Answer: '{correct_answer}' | {status}")
    
    print("\n4. 📄 Study Document Generation Demo:")
    sample_correct_questions = chemistry_questions[:3]
    study_doc = science_agent.generate_study_document("Chemistry", sample_correct_questions)
    print(f"   Generated study document ({len(study_doc)} characters):")
    print("   " + "─" * 40)
    print("   " + study_doc[:500] + "..." if len(study_doc) > 500 else study_doc)
    print("   " + "─" * 40)
    
    print("\n5. 🤖 Multi-Agent Architecture:")
    print("   ├── Science2UCoordinator (Main Agent)")
    print("   ├── QuestionGenerator (Specialized Agent)")
    print("   ├── AnswerEvaluator (Specialized Agent)")
    print("   ├── DocumentGenerator (Specialized Agent)")
    print("   ├── ProgressTracker (Specialized Agent)")
    print("   └── QuizLoop (Loop Agent)")
    print("       ├── QuestionPresenter")
    print("       ├── AnswerChecker")
    print("       └── ProgressEvaluator")
    
    print("\n6. 🎓 Key Features Applied from 5-Day Course:")
    features = [
        "✅ Multi-agent systems (Sequential, Parallel, Loop)",
        "✅ Custom tools and function tools",
        "✅ Session management and memory",
        "✅ Agent observability with LoggingPlugin",
        "✅ Context engineering and state management",
        "✅ Agent evaluation and progress tracking",
        "✅ Production-ready architecture"
    ]
    
    for feature in features:
        print(f"   {feature}")
    
    print("\n7. 📊 Question Bank Statistics:")
    total_questions = 0
    for topic, questions in science_agent.question_banks.items():
        count = len(questions)
        total_questions += count
        difficulty_counts = {}
        for q in questions:
            diff = q['difficulty']
            difficulty_counts[diff] = difficulty_counts.get(diff, 0) + 1
        
        print(f"   {topic}: {count} questions", end="")
        if difficulty_counts:
            diff_str = ", ".join([f"{k}:{v}" for k, v in difficulty_counts.items()])
            print(f" ({diff_str})")
        else:
            print()
    
    print(f"   Total: {total_questions} questions across {len(science_agent.topics)} topics")
    
    print("\n8. 🚀 Ready to Start Learning!")
    print("   Run 'python science2u_agent.py' to begin your interactive learning session!")
    
    print("\n" + "=" * 50)
    print("Demo completed! Science2U is ready for educational adventures! 🎓")

if __name__ == "__main__":
    # Load environment variables
    load_dotenv()
    
    if not os.getenv("GOOGLE_API_KEY"):
        print("⚠️  Note: GOOGLE_API_KEY not set. Demo will show structure only.")
        print("   Set your API key in .env file to run the full interactive agent.")
    
    asyncio.run(demo_science2u())