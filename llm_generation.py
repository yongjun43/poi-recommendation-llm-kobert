import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

MODEL = "beomi/KoAlpaca-Polyglot-5.8B"


def build_generator(model_name: str = MODEL):
    use_cuda = torch.cuda.is_available()
    torch_dtype = torch.float16 if use_cuda else torch.float32

    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        torch_dtype=torch_dtype,
        low_cpu_mem_usage=True,
    )
    model.eval()

    if use_cuda:
        model.to("cuda")
        device = 0
    else:
        model.to("cpu")
        device = -1

    return pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
        device=device,
    )


pipe = build_generator()


def ask(
    question: str,
    context: str = "",
    max_new_tokens: int = 128,
    temperature: float = 0.7,
    top_p: float = 0.9,
):
    prompt = (
        f"### 질문: {question}\n\n### 맥락: {context}\n\n### 답변:"
        if context
        else f"### 질문: {question}\n\n### 답변:"
    )

    ans = pipe(
        prompt,
        do_sample=True,
        max_new_tokens=max_new_tokens,
        temperature=temperature,
        top_p=top_p,
        return_full_text=False,
        eos_token_id=2,
    )
    return ans[0]["generated_text"].strip()


if __name__ == "__main__":
    print(ask("동성로에 대해서 설명해줘"))
