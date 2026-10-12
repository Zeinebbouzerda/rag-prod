\# Journal d'évaluation du projet RAG (doc FastAPI)



\## Configuration de base

\- Corpus : documentation FastAPI (Markdown), 491 chunks

\- Chunking : 300 mots, chevauchement 50

\- Embeddings : intfloat/multilingual-e5-small

\- Base vectorielle : Qdrant (mode local)

\- LLM : gemini-3.5-flash-lite (le juge est le même modèle que le générateur)



\## Tableau d'ablation



| Configuration | recall@5 facile (27) | hard\_en (10) | fr (10) | Fidélité | Refus |

|---|---|---|---|---|---|

| Baseline (300 mots, e5-small, vectoriel) | 92,6 % | 70 % | 80 % | 5/5 | 5/5 |



\## Observations

\- Les questions reformulées (hard\_en) sont plus dures que le français : le problème principal est le décalage de vocabulaire entre la question et la doc.

\- Raté facile 1 : "run a task after returning a response" (mots différents de la doc).

\- Raté facile 2 : "OAuth2 password authentication" : la page obtenue (simple-oauth2.md) est valable, donc métrique trop stricte.

\- 3 chunks sur 5 viennent parfois de la même page : manque de diversité.



\## Limites

\- Fidélité mesurée sur 5 questions seulement.

\- Juge = même modèle que le générateur (indulgent).

\- Seulement 10 questions par groupe difficile : 1 question = 10 points.



\## Ce qui n'a pas marché

\- gen\_questions.py : quota gratuit Gemini épuisé (429), questions écrites à la main à la place.

