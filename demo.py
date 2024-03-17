from openai import OpenAI

client = OpenAI(api_key='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')

def get_gpt_analysis(anxietyscore, depressionscore, stressscore):
    # Use ChatGPT API for detailed analysis
    prompt = f"Provide a detailed analysis for a user with Anxiety Score: {anxietyscore}, Depression Score: {depressionscore}, Stress Score: {stressscore}"

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a mental health analysis assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=300  # You can adjust this value based on the desired response length
    )

    analysis_result = response.choices[0].message.content
    print(analysis_result)
    return analysis_result

get_gpt_analysis(28, 28, 28)
