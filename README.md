# AIDOaRt-UNISS-ReqH

ReqH is a tool designed to streamline the translation of natural language requirements into Property Specification 
Patterns (PSPs). It leverages Large Language Models (LLMs), which are known for their ability to understand and 
generate human-like text. It is imperative to acknowledge that the outcomes produced by ReqH are heavily reliant 
on the chosen LLM and the context provided to it, thus potentially yielding flawed results.

## Requirements
ReqH requires [LangChain](https://github.com/langchain-ai/langchain) and 
[Ollama](https://github.com/ollama/ollama) to be installed. We refer to the official installation guides
of this two tools:
- [LangChain Installation Guide](https://python.langchain.com/docs/get_started/installation)
- [Ollama Installation Guide](https://github.com/ollama/ollama)

Additionally, Ollama should be running during the execution of ReqH and the LLM of interest should be downloaded
using the `ollama pull <model_id>` command. For more information we refer to the official documentation.

## How to use
ReqH can be executed launching [main.py](main.py) and requires four command line parameters:
- `--input_path`: Path to the Plain Text file containing the requirements in natural language to translate in PSP. 
It should contain one requirement for each row. An example can be found in [input.txt](inputs/input.txt).
- `--output_path`: Path to the Plain Text file that will contain the requirements translated in PSP.
It will contain one requirement for each row. An example can be found in [output.txt](outputs/output.txt).
- `--context_path`: Path to the Plain Text file containing the context to provide to the LLM model.
An example can be found in [context.txt](inputs/context.txt).
- `--config_path`: Path to the .ini file containing the configuration info for the script.
An example can be found in [default_config.ini](configs/default_config.ini).

## Important Notes

- Different LLMs than the one presented in the Ollama Library can be used leveraging the 
[LangChain LLMs Module](https://python.langchain.com/docs/integrations/llms/) and slightly changing the relevant 
code in [main.py](main.py).
- If new variables are added in the config file, minor modification of the code in [main.py](main.py) will be needed
to manage them.
