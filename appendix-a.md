Appendix A – AI Support and Project Decision Record (CA2)
Project overview
This document records the main ideas I considered while working on CA2, the decisions I made, and how I planned and checked the project. I used AI as a support tool to help me understand some topics and to guide decisions during planning. I reviewed the suggestions and adapted them to the project and to my own implementation.

The project focuses on four security vulnerabilities. For each one, I created an example of vulnerable code, a test to demonstrate the problem, and a safer version. The main goal is to understand how the issue happens and how the mitigation changes the result.
1. General project structure
I kept the same structure for the four vulnerability folders so the project would be easier to run and compare. The vulnerable and mitigated versions use the same function names and arguments. The main difference is how the code works internally.

The exploit.py file accepts a command-line argument to choose which version to test. It imports that version and runs the test. The output clearly indicates whether the test was successful or blocked. The script uses exit code 0 when the expected vulnerable behaviour is demonstrated and exit code 1 when it is not.

I planned to use only Python's standard library, including modules such as sqlite3, hashlib, secrets, threading, os and tempfile. This avoids extra installation steps and makes it easier for someone else to run the project. The full test should take less than five minutes.

I also used new examples and names instead of reusing my Secure Notes CA1 project. This helps keep the projects separate. Table names, functions and comments should be different from the earlier assignment.
2. SQL Injection – 01-injection/
What I wanted to demonstrate
SQL Injection happens when user input is added directly to an SQL query. In this example, the search function builds the query by joining the input with the SQL string. This can allow the input to change the query's logic.
vulnerable.py
- Create a small SQLite database in memory using :memory:.
- Add a table with three or four example records. One record should be private or otherwise not normally visible.
- Create a search function, for example by name or category, that builds its SQL query using string concatenation or an f-string.
- Add a short comment explaining that user input becomes part of the SQL command, which is the main problem.
exploit.py
- Call the search function using a malicious input that changes the query and returns records that a normal search would not show.
- First run a normal search so the output can be compared with the attack.
- The test should have a clear success condition: the private record appears in the results.
- Use an example payload based on class material or the OWASP SQL Injection Prevention Cheat Sheet, and mention the source in a code comment.
mitigated.py
Use the same search function, but with a parameterised query and SQLite placeholders (?). If user input is used for a column name or sorting option, parameters cannot be used for those parts. In that case, use an allow-list of accepted values.
Report notes
Explain how mixing data and SQL code creates the vulnerability, show the example and test, and describe the mitigation. Also mention the limitation: parameterisation does not protect SQL identifiers, and using raw SQL in an ORM can introduce similar risks again.
3. IDOR – 02-idor/
What I wanted to demonstrate
This example shows the difference between authentication and authorisation. A function may check that a user is logged in but still fail to check whether the requested resource belongs to that user.
vulnerable.py
- Create an in-memory database with two users and resources belonging to each user. Use a new example domain, such as invoices, recipes or orders.
- Create a function that receives the current user and a resource ID.
- The function returns the resource based only on its ID and does not check its owner.
- Add a comment explaining that authentication is present, but authorisation is missing.
exploit.py
- User A requests a resource ID belonging to User B.
- Sequential IDs can make other resources easier to guess, so this should be explained as part of the example.
- The test is successful if User A receives User B's information.
- Also test that User A can access their own resource in both versions, to show that the mitigation does not break normal use.
mitigated.py
Include the ownership check in the database query. A resource should only be returned if it belongs to the current user. If the resource does not exist or belongs to another user, return the same “not found” response. This avoids confirming that another user's resource ID exists.
Report notes
The ownership check protects each query, but it is not a structural protection. Every new function must remember to include the owner filter, and missing it can create the same problem again. Other options include a central access layer that always applies ownership rules or row-level security. UUIDs can make IDs harder to guess, but using UUIDs alone does not fix the authorisation problem.
4. Cryptographic misuse – 03-crypto-misuse/
What I wanted to demonstrate
This example looks at passwords stored using a fast hash without a salt. A fast hash can be useful for file integrity checks, but it is not a good choice for password storage because it makes guessing passwords much faster. Without a salt, users with the same password also have the same hash.
vulnerable.py
- Include the functions register(user, password) and verify(user, password).
- Store passwords using a fast general-purpose hash such as SHA-256, without a salt.
- Add a comment explaining why this approach is weak for password storage and why identical passwords produce identical hashes.
exploit.py
Simulate a situation where the database has been leaked and an attacker has access to the password hashes.
- Register a few users, including two users with the same weak password.
- Show that the two users have identical hashes when no salt is used.
- Use a small list of common passwords (around 10–20 entries) to test password guesses against a hash.
- Measure the time for each attempt with time.perf_counter().
- The test should show either that a password was recovered or that identical hashes were identified.
mitigated.py
Use a slower password derivation function with a salt, such as hashlib.scrypt, with suitable parameters based on OWASP guidance. Generate a random salt for each user with secrets. Use hmac.compare_digest when comparing derived values.

The test should show that the same password produces different stored values when different salts are used, and that checking guesses takes more time.
Testing and limitations
A weak password can still be guessed when scrypt is used. The function does not make password guessing impossible; it increases the cost. Define the test clearly, for example by checking whether a password can be recovered within a fixed budget or by demonstrating that repeated passwords no longer produce the same stored hash. The final version gives both implementations the same 0.5-second time budget (see section 15), so the difference in outcome comes only from the cost of the hash function. Record the measured cost difference. In the critical evaluation, explain that password hashing reduces risk but does not replace strong password choices or login attempt limits.
5. TOCTOU / Race condition – 04-toctou/
What I wanted to demonstrate
A Time-of-Check to Time-of-Use problem can happen when a program checks a condition and then acts on it, but the state changes between those two steps. A simple example is checking an account balance before withdrawing money.
vulnerable.py
- Create an account with an initial balance, for example 100.
- Write a withdraw(amount) function that reads the balance, checks whether there is enough money, waits briefly, and then updates the balance.
- Use a short time.sleep() to make the race window easier to reproduce. This represents work that could happen during a database or network operation.
- Add a comment explaining that the balance can change between the check and the update.
exploit.py
- Start multiple threads using threading.
- Make the threads try to withdraw amounts that, together, are more than the original balance.
- The test succeeds if the total withdrawn is greater than the initial balance or the final balance becomes negative or inconsistent.
- Run the test several times, such as 20 attempts, and report how often it happens. Race conditions are not guaranteed to happen every time, so the results should show this limitation.
mitigated.py
Make the check and update atomic by using a threading.Lock around the critical section. The expected result is that the total withdrawn never goes above the original balance across the test runs.
Report notes
Explain why race conditions can be difficult to find with normal testing because the problem is not always reproduced. Also explain that a local lock is not enough when multiple processes or servers are involved. In a real database, the operation should be protected by an atomic update or transaction. For file operations, the classic TOCTOU issue can happen when a program checks access with os.access() and then opens the file separately; safer handling should use the opened file descriptor and avoid relying on a separate check.
6. Test evidence – test_output.txt
The test_output.txt file in each folder should be generated by run_all.sh, not written manually. It should include:
- The date and time of the test and the Python version.
- The exploit output when testing the vulnerable version, showing RESULT: EXPLOITED.
- The exploit output when testing the mitigated version, showing RESULT: BLOCKED.
This output is evidence for the Testing and Evidence section of the report. Screenshots should be taken from the new CA2 test results, not reused from CA1.
7. Test runner – run_all.sh
The runner should follow these steps:
1. Stop if an unexpected error happens (set -euo pipefail), but do not stop just because an exploit returns its expected failure code. Capture the exit code for each test.
2. For each of the four vulnerability folders, run the exploit against the vulnerable version and record the exit code.
3. Run the exploit against the mitigated version and record its exit code.
4. Save both outputs to that folder's test_output.txt using tee.
5. At the end, print a summary table with eight rows. It should show the vulnerability, version, expected result, actual result and whether it passed (OK) or failed (FAILED).
6. Return exit code 0 only when all eight results match the expected outcomes: four vulnerable tests are exploited and four mitigated tests are blocked.
Remember to make the script executable with chmod +x run_all.sh.
8. README
The README should include the following information:
- A short description of the repository: four vulnerability types, each with vulnerable, exploit and mitigated code.
- Requirements, including the Python version actually used and that no external packages are needed.
- The exact command to run all tests and what the user should expect to see (the eight-row summary, with all checks passing).
- How to run one vulnerability test separately, including the exploit command and argument.
- A short explanation of each folder.
- A warning that the vulnerable examples are for academic purposes only and must not be used in production.
- A final check: copy the project to another location or a clean environment and follow the README exactly. If extra steps are needed, the README should be updated.
9. Appendix A and source notes
For the AI support record, include the date, tool, original prompt when required by the assignment, output, and a short explanation of what I accepted, changed or rejected and why. Include this interaction if it is part of the record.

For sources.md (originally fontes.md), review the candidate papers for each topic. Check the year and publication details in the PDF itself, save the papers, and write notes for each topic. Use the four questions or tensions already identified in the notes as the starting point for the literature review.
10. Work priorities
The suggested order was based on the deadline and the marks available:
Priority	Task	Marks
1	Complete the four code examples, starting with IDOR and SQL Injection	20 + part of 25
2	Finish run_all.sh, test_output.txt and README evidence	20
3	Write the four technical analysis sections	25
4	Complete the literature review using the source notes	25
5	Critical evaluation, final argument and conclusion	15 + 15
6	Harvard references, AI declaration and final PDF integrity check	—


If time is limited, it is better to complete and explain two vulnerability examples properly than to leave four unfinished. However, because the brief asks for four, I should aim to have at least a basic working version of each.
11. Folder checklist
Use this checklist for each vulnerability:
- [ ] vulnerable.py runs without errors and includes a comment explaining the weakness.
- [ ] mitigated.py uses the same functions, names and arguments as the vulnerable version.
- [ ] The exploit against the vulnerable version shows RESULT: EXPLOITED and returns exit code 0.
- [ ] The exploit against the mitigated version shows RESULT: BLOCKED and returns exit code 1.
- [ ] Normal use works in both versions.
- [ ] test_output.txt is generated by the runner.
- [ ] The example domain and names are different from CA1.
- [ ] The prompts used are recorded in appendix-a.md, as required.
12. Test summary
The terminal summary provided for this run showed the expected result for all eight checks:
Vulnerability	Version	Expected	Actual	Status
01-injection	vulnerable	EXPLOITED (code 0)	EXPLOITED (code 0)	OK
01-injection	mitigated	BLOCKED (code 1)	BLOCKED (code 1)	OK
02-idor	vulnerable	EXPLOITED (code 0)	EXPLOITED (code 0)	OK
02-idor	mitigated	BLOCKED (code 1)	BLOCKED (code 1)	OK
03-crypto-misuse	vulnerable	EXPLOITED (code 0)	EXPLOITED (code 0)	OK
03-crypto-misuse	mitigated	BLOCKED (code 1)	BLOCKED (code 1)	OK
04-toctou	vulnerable	EXPLOITED (code 0)	EXPLOITED (code 0)	OK
04-toctou	mitigated	BLOCKED (code 1)	BLOCKED (code 1)	OK


The full outputs are stored in each folder's test_output.txt. The project also includes run_all.sh, README.md and the source notes in sources.md.
13. Decisions and changes
I followed the general project scope and testing approach, but I adapted the instructions to the Python version available on my system. An earlier run used Python 3.13.12; the final recorded runs and figures were produced with Python 3.13.9 on macOS, and the README records this version.

The reference to Green & Smith is still marked as pending because I could not access the PDF. I did not treat it as a source I had fully read.
14. Why I made these decisions
I wanted to keep the project based on the standard Python library and use tests that could be repeated. I also wanted to be clear about the Python version and about any source that I could not verify. This helps avoid claiming that something was tested or read when it was not.

AI was used as a support tool to help me understand some ideas and consider options during planning. I made adjustments to the guidance based on the project requirements, my environment and the tests I ran.

15. AI-assisted changes made with Claude Code (21–22 November 2026)
Tool: Claude Code (Anthropic), desktop app, model Claude Opus 5.5. The AI worked directly on the project folder. Everything listed below was produced or changed by the AI at my request; I reviewed each change and re-ran the tests afterwards.

Prompts (verbatim, translated from Portuguese in brackets):
- 21 Nov: "faca as alteracoes nescessarias no projeto se quiser conferir o ca1 ele esta no desktop" followed by my pasted CA2 plan. [Make the necessary changes to the project; CA1 is on the desktop if you want to check it.] The AI stopped generating the code files after a safety filter interrupted its response, so I wrote the four vulnerable, exploit and mitigated files myself.
- 21 Nov: "muito bem faca o texto de oq tenho que fazer em cada file do projeto bem explicado e me guiando" [Write a text explaining what I have to do in each file, guiding me.] Output: a guide (GUIA.md) describing what each file had to contain and demonstrate, without code. Sections 1–11 of this appendix are based on that guide.
- 21 Nov: "fiz o projeto analise e ve oq acha tambnem se puder deixar tudo em ingles" [I did the project, analyse it and tell me what you think; also translate everything to English if possible.] Output: a review and a translation of the output messages, function names (registar/verificar/levantar became register/verify/withdraw), run_all.sh, README.md and fontes.md (renamed sources.md); apendice-a.md was renamed appendix-a.md. The review identified that the crypto exploit gave the vulnerable version 12 attempts and the mitigated version only 3, so the mitigated result came from the smaller budget rather than from scrypt.
- 22 Nov: "Sim, corrige" [Yes, fix it.] Output: the crypto exploit now uses the same 0.5-second time budget for both versions, counts SHA-256 time as attacker cost and prints the guess rate. Measured result: about 660,000 guesses per second with SHA-256 against about 3 per second with scrypt, a cost ratio of roughly 10^4 that varies between runs.
- 22 Nov: "faca um sistema para tirar print dos resultados etc e tudo que for importante para o trablho" [Make a system to take screenshots of the results and everything important for the work.] Output: tools/capture_evidence.py, which runs run_all.sh and generates 13 figures, EVIDENCE.md with suggested captions, an HTML gallery and manifest.json with the SHA-256 of every source file. This script was written entirely by the AI and needs Pillow.
- 22 Nov: "show oq falta eu fazer ?" and "Sim, atualiza" [What is left for me to do? / Yes, update it.] Output: a list of remaining tasks and the corrections to this appendix.

What I accepted, changed or rejected, and why:
- Accepted the translation and the crypto time-budget fix, because the original unequal budget would have made the comparison unfair.
- Accepted the evidence script because it generates figures directly from the saved test output, so the numbers in the report match the evidence.
- Kept my own design decisions for the four vulnerability examples. The report text, the literature review and the final argument are my own writing.

