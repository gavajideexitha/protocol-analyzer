"""Optional LangChain explanation layer. Works only when API credentials are configured."""
import os

def explain_with_llm(packet_summaries):
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return "LLM analysis skipped: OPENAI_API_KEY is not configured."

    try:
        from langchain_openai import ChatOpenAI
        from langchain_core.messages import SystemMessage, HumanMessage
        model_name = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        llm = ChatOpenAI(model=model_name, temperature=0, api_key=api_key)
        # Send compact metadata only; do not send full packet payloads.
        compact = packet_summaries[:100]
        prompt = (
            "Analyze these packet metadata records from a small localhost networking lab. "
            "Explain the observed TCP communication, identify HTTP indicators, and mention "
            "any limitations. Do not claim an attack or vulnerability without evidence. "
            "These records are observations, not proof of malicious activity.\n\n"
            f"{compact}"
        )
        result = llm.invoke([
            SystemMessage(content="You are a cautious network-protocol teaching assistant."),
            HumanMessage(content=prompt),
        ])
        return result.content
    except Exception as exc:
        return f"LLM analysis unavailable: {type(exc).__name__}: {exc}"
