import io
import os
import zipfile
from pathlib import Path

import vertexai
from vertexai.generative_models import GenerativeModel, Part


def gen_readme(content: bytes, output_path: Path) -> None:
    # open zip file
    extract_path = output_path / "input"
    with zipfile.ZipFile(io.BytesIO(content)) as z:
        z.extractall(extract_path)

    # read sources and create Part object
    parts: list[str | Part] = [
        "Read following program code and output the summary in markdown format"
    ]
    for root, _, files in os.walk(extract_path):
        for filename in files:
            file_path = os.path.join(root, filename)
            with open(file_path, "rb") as f:
                data = f.read()
                part = Part.from_data(data=data, mime_type="text/plain")
                parts.append(part)

    vertexai.init(project="code-caster", location="asia-northeast1")

    gemini_model = GenerativeModel("gemini-1.5-pro-preview-0409")
    model_response = gemini_model.generate_content(parts)  # type: ignore

    # get reponse text
    response_text = model_response.candidates[0].content.parts[0].text

    # remove code block "```" of start and end
    if response_text.startswith("```markdown"):
        response_text = response_text[len("```markdown") :].strip()
    if response_text.endswith("```"):
        response_text = response_text[: -len("```")].strip()

    # converts escaped newline characters to actual newlines
    response_text = response_text.replace("\\n", "\n")

    output_file = output_path / "output.md"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(response_text)
