# Populate README.md
*Example*
- **Intended Function:** Describe what the code is designed to do, including its main purpose and functionality.
- **Internal Resources:** Specify if the code interacts with any internal systems or resources, and list them if applicable.
- **Credentials Required:** Indicate whether credentials are needed to run the code, and mention the type if necessary.
- **Trigger Mechanism:** Explain how the code is initiated or triggered (e.g., manually, via API call, on a schedule).

## Template Files
#### .gitignore
> Default is a combination of build artifacts, OS generated files

> The `.gitignore` file specifies intentionally untracked files that Git should ignore. It is used to prevent committing files such as build outputs, dependency directories, sensitive information, or other files that do not need to be version controlled. Patterns defined in this file help keep the repository clean and focused only on relevant source code and configuration files.
[text](https://docs.github.com/en/get-started/git-basics/ignoring-files)

#### .dockerignore
> Default ignores all, to promote specifying only required context being passed to build. 

> The `.dockerignore` file lists files and directories that should be excluded from Docker build context. This helps reduce build time, avoid copying unnecessary files into Docker images, and prevent sensitive or irrelevant files from being included in the final image. [text](https://docs.docker.com/build/concepts/context/#dockerignore-files)