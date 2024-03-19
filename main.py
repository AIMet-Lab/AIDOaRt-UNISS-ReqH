import argparse
import pathlib
import configparser

from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

import utilities


def make_parser() -> argparse.ArgumentParser:

    parser = argparse.ArgumentParser("REQuirement Helper for the AIDOaRt Project")

    input_path_help = "Path to the Plain Text file containing the requirements in natural language to translate in" \
                      " PSP. It should contain one requirement for each row."
    parser.add_argument("--input_path", type=str, help=input_path_help, default="inputs/input.txt")

    output_path_help = "Path to the Plain Text file that will contain the requirements translated in PSP. " \
                       "It should contain one requirement for each row."
    parser.add_argument("--output_path", type=str, help=output_path_help, default="outputs/output.txt")

    context_path_help = "Path to the Plain Text file containing the context to provide to the LLM model."
    parser.add_argument("--context_path", type=str, help=context_path_help, default="inputs/context.txt")

    config_path_help = "Path to the .ini file containing the configuration info for the script."
    parser.add_argument("--config_path", type=str, help=config_path_help, default="configs/default_config.ini")

    return parser


if __name__ == "__main__":

    # Parse the command line parameters.
    arg_parser = make_parser()
    args = arg_parser.parse_args()

    input_path = args.input_path
    output_path = args.output_path
    context_path = args.context_path
    config_path = args.config_path

    # Extract configuration info.
    config = configparser.ConfigParser()
    _ = config.read(config_path)

    llm_id = config["DEFAULT"]["llm_id"]
    temperature = config["DEFAULT"].getfloat("temperature")
    verbose = config["DEFAULT"].getboolean("verbose")

    # Instantiate loggers.
    stream_log, file_log = utilities.instantiate_logger(output_path)

    stream_log.info(f"Initializing Inputs and Configuration...")

    # Extract text from the context file and save it as a single string.
    context = pathlib.Path(context_path).read_text()

    # Extract the natural language requirements from the input file and save them in a list.
    input_text = pathlib.Path(input_path).read_text()
    nl_req_list = str.split(input_text, "\n")
    nl_req_list[:] = [x for x in nl_req_list if x]  # If the user wrote some empty line we need to remove them.

    # Instantiate the Large Language Model of interest.
    stream_log.info(f"Instantiating LLM {llm_id}, Parsers and Chains...")

    llm = Ollama(model=llm_id, temperature=temperature)

    # Define the form of the prompt which will be given to the LLM
    prompt = ChatPromptTemplate.from_messages([
        ("system", ""),
        ("user", "{input}")
    ])

    # Instantiate the Output Parser.
    output_parser = StrOutputParser()

    # Define the LangChain between prompt, llm, and output parser
    chain = prompt | llm | output_parser

    # Now, we need to cycle over the list of natural language requirements and consider them one at a time.
    stream_log.info("Translating...")

    for nl_req in nl_req_list:

        if verbose:
            stream_log.info(f"Translating Requirement: {nl_req}")

        # Invoke the chain previously defined.
        psp_req = chain.invoke({"input": context + nl_req})
        psp_req = psp_req.replace("\n", " ")

        if verbose:
            stream_log.info(f"Translated Requirement: {psp_req}")

        file_log.info(f"{psp_req}")

    stream_log.info("Translation complete!")
