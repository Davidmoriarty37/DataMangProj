# DataMangProj

Data Sources:
https://docs.github.com/en/rest/search/search?apiVersion=2026-03-10#search-issues-and-pull-requests
https://github.com/scipy/scipy/labels?page=3
https://www.kaggle.com/datasets/coderanand/university-query-priority-classification
https://data.stackexchange.com/stackoverflow/query/edit/1943008

Github api documentation: https://docs.github.com/en/rest/search/search?apiVersion=2026-03-10#search-issues-and-pull-requests

Query i used on https://data.stackexchange.com/stackoverflow/query/edit/1943008 is below:

<img width="251" height="203" alt="Screenshot 2026-03-28 at 1 42 13 PM" src="https://github.com/user-attachments/assets/36f8088a-76d2-478d-bc22-65b36e10d850" />


Kaggle: priority labels already exist (Low/Medium/High), direct passthrough, no inference needed.

GitHub scipy: no native priority field, so we start with the title prefix which is a community convention in scipy. BUG is always High. Ambiguous labels like MAINT, BLD, DEP, CI start at Medium, then we scan the description text for urgency keywords (error, crash, security, etc.) and bump up one level if found. DOC, TST, BENCH are Low. Anything unrecognized defaults to Medium.

Stack Overflow: no priority field, so we classify from the question text. Urgency keywords (error, crash, broken, etc.) map to High, help-seeking keywords (how to, difference between, etc.) map to Medium, and questions matching neither default to Low unless score is above 3000, then Medium since high-vote questions are still widely encountered problems.
