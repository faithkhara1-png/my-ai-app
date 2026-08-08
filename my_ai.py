from langchain_ollama import OllamaLLM

# Local AI model ko connect kar rahe hain
ai = OllamaLLM(model="llama3.2")

print("==========================================")
print("   AAPKA PERSONAL FREE AI READY HAI!   ")
print("   (Band karne ke liye 'exit' likhein)   ")
print("==========================================\n")

while True:
    user_input = input("Aap: ")
    if user_input.lower() == 'exit':
        print("AI: Alvida! Phir milenge.")
        break
    
    if user_input.strip() == "":
        continue

    response = ai.invoke(user_input)
    print(f"\nAI: {response}\n")