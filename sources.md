# Sources and reading notes — CA2

## Verification status

Where indicated, the years and publication details below were checked against the first page of the PDFs saved in [`literature/pdfs/`](literature/pdfs/). Journal articles have no conference city; for those I record the journal and issue. The Green and Smith PDF is still pending: the old mirror returned an error and open access to the IEEE page only provided metadata, so I do not treat it as a completed reading or as a final source.

| Theme | Confirmed reference | Year and venue as stated in the document | Local PDF |
|---|---|---|---|
| Developer | Naiakshina et al., *Why Do Developers Get Password Storage Wrong?* | CCS ’17, 30 Oct.–3 Nov. 2017, Dallas, TX, USA; pp. 311–328 | [PDF](literature/pdfs/naiakshina-2017-ccs.pdf) |
| Developer | Naiakshina et al., *“If you want, I can store the encrypted password.”* | CHI 2019, 4–9 May 2019, Glasgow, Scotland; 12 pp. | [PDF](literature/pdfs/naiakshina-2019-chi.pdf) |
| Developer | Votipka et al., *Understanding Security Mistakes Developers Make* | 29th USENIX Security Symposium, 2020; pp. 109–126. The PDF names the symposium and dates but prints no city. | [PDF](literature/pdfs/votipka-2020-usenix.pdf) |
| Tools | Johnson et al., *Why Don’t Software Developers Use Static Analysis Tools to Find Bugs?* | ICSE 2013, San Francisco, California, USA; pp. 672–681 | [PDF](literature/pdfs/johnson-2013-icse.pdf) |
| Tools | Tiganov, Do and Ali, *Designing UIs for Static-Analysis Tools* | [*Communications of the ACM*](https://doi.org/10.1145/3486600), 65(2), Feb. 2022, pp. 52–58; the ACM reference gives New York, USA. The saved open-access PDF is the earlier version of the same article in *ACM Queue*, Jul.–Aug. 2021. | [PDF](literature/pdfs/tiganov-2021-acm-queue.pdf) |
| Process | Assal and Chiasson, *Security in the Software Development Lifecycle* | SOUPS 2018, 12–14 Aug. 2018, Baltimore, Maryland, USA; pp. 281–296 | [PDF](literature/pdfs/assal-2018-soups.pdf) |
| Process | Assal and Chiasson, *“Think secure from the beginning”* | CHI 2019, 4–9 May 2019, Glasgow, Scotland; 13 pp. | [PDF](literature/pdfs/assal-2019-chi.pdf) |
| APIs | Green and Smith, *Developers are Not the Enemy!* | *IEEE Security & Privacy*, 14(5), Sep.–Oct. 2016, pp. 40–46. Journal article, no conference venue. Metadata and abstract from the [research group](https://www.besec.uni-bonn.de/publications/developers-are-not-the-enemy-the-need-for-usable-security-apis) confirm these details; PDF not saved. | Pending |
| APIs | Nadi et al., *“Jumping Through Hoops”* | ICSE ’16, 14–22 May 2016, Austin, Texas, USA; pp. 935–946 | [PDF](literature/pdfs/nadi-2016-icse.pdf) |
| APIs | Egele et al., *An Empirical Study of Cryptographic Misuse in Android Applications* | CCS ’13, 4–8 Nov. 2013, Berlin, Germany; pp. 73–84 | [PDF](literature/pdfs/egele-2013-ccs.pdf) |

## Notes by theme

### 1 — Developer behaviour

- **Naiakshina et al. (2017):** qualitative study of 20 computer science students implementing registration and authentication. Explicitly requested security and the supporting APIs/frameworks affect the outcome, but stated knowledge does not guarantee practical application. The student sample and controlled task limit generalisation to professional teams.
- **Naiakshina et al. (2019):** field study with freelancers hired for a password-storage task. The pattern of insecure implementation without an explicit request also appears outside the lab; the authors report misconceptions and outdated methods. The hiring context and short tasks are not equivalent to long-term development inside an organisation.
- **Votipka et al. (2020):** qualitative analysis of 94 submissions to a secure-programming contest, including 866 exploits. Mistakes rooted in misunderstanding security concepts appear more often than simple slips. This contradicts an explanation that attributes all defects to the API interface, although the contest does not represent all product development.

### 2 — Tool gaps

- **Johnson et al. (2013):** interviews with 20 developers show that false positives, presentation and comprehension of warnings create friction. The study offers plausible reasons for abandonment, but it is qualitative and does not measure adoption across the industry.
- **Tiganov, Do and Ali (2022; open version in ACM Queue 2021):** apply interface guidelines to SWAN, a static analysis tool for Swift. They highlight workflow integration, fast feedback and actionable explanations. It is a source on design and usability; on its own it does not show a general reduction of vulnerabilities in production.

### 3 — Time pressure and process

- **Assal and Chiasson (2018):** interviews with 13 developers from teams in 15 North American companies. Practices vary, and division of labour, culture, knowledge, external pressure and incidents shape how much room security gets. The small qualitative sample explains mechanisms, not prevalence.
- **Assal and Chiasson (2019):** online survey of 123 developers employed in North America. The authors stress that a lack of organisational and process support often explains the obstacles, despite stated motivation. It is cross-sectional self-report and does not prove causation.

### 4 — Security–usability trade-off in APIs

- **Green and Smith (2016):** argue that treating the developer as an adversary hides design flaws, and that security APIs should be centred on the developer's work. A useful conceptual position for framing the hypothesis, but the PDF has not been retrieved and this reference should not be cited as a completed reading until that is resolved.
- **Nadi et al. (2016):** triangulate 100 Stack Overflow questions, 100 Java repositories and responses from 48 developers. Participants struggle with the details of using cryptographic APIs even when they correctly identify the high-level concepts; they ask for more task-oriented solutions. This supports API-level interventions, but the focus is Java cryptography.
- **Egele et al. (2013):** analyse 11,748 Android applications that use cryptographic APIs; 10,327 (88%) contain at least one error detectable by CryptoLint. This shows the scale and feasibility of automated analysis on that dataset, not that 88% of all applications, or of all password storage, is insecure.

## Tensions for the critical synthesis

1. **API or conceptual understanding?** Green and Smith and Nadi et al. point to difficult APIs and insufficient support. Votipka et al. find many errors of conceptual understanding. The explanations can coexist: safer APIs and high-level tasks reduce dangerous choices, while teaching and review still matter when the mental model is wrong.
2. **Knowledge or explicit requirement?** Naiakshina et al. show that knowing passwords must be protected is not enough when the task does not ask for security. An explicit requirement can shift priorities; secure defaults make that protection less dependent on someone remembering to ask for it.
3. **Individual or organisation?** Assal and Chiasson attribute part of the problem to responsibilities, time and organisational support. Individual training alone does not resolve competing priorities or the lack of an owner for security tasks.
4. **Tool available or tool adopted?** Johnson et al. document friction and difficulty interpreting warnings; the user-centred proposal of Tiganov et al. suggests integration improvements. Automated analysis only helps if its feedback is reliable, understandable and embedded in the workflow.

## Industry data — not academic literature

The Microsoft Security Response Center post of 16 July 2019 attributes roughly 70% of the CVE-assigned vulnerabilities Microsoft addressed to memory-safety issues. It is data from one organisation about one class of bugs; it is neither an estimate for all vulnerabilities nor a peer-reviewed study, and should be presented with that limitation. Source: [MSRC, “A proactive approach to more secure code”](https://www.microsoft.com/en-us/msrc/blog/2019/07/a-proactive-approach-to-more-secure-code).

## Technical references used in the code

- Current OWASP guidance recommends scrypt, where Argon2id is unavailable, with N=2¹⁷, r=8 and p=1; these are the parameters used in the demonstration: [OWASP Password Storage Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html).
- The boolean `OR` pattern in the SQLi example is illustrative; the prevention source for the mitigation is the [OWASP SQL Injection Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html).
