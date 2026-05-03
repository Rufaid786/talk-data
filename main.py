from agent import build_snowflake_agent


def process_query(agent):
    print("Welcome to the Snowflake Query Agent!")
    while True:
        try:
            question=input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break
        if not question:
            continue
        if question.lower() in {"exit", "quit", "bye"}:
            print("Goodbye!")
            break

        print(f"Agent is processing your query... {question}")
        result=agent.invoke({"message":[{"role":"user", "content":question}]})    
        print(result["messages"][-1]["content"])

if __name__ == "__main__":
    agent=build_snowflake_agent()
    process_query(agent)