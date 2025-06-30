def get_prompt(role: str, question: str, knowledge: str) -> str:
    if role == "HR":
        return f"""
Olet asiantunteva HR-avustaja suomalaisessa yrityksessä.
Vastaa työntekijöiden kysymyksiin alla olevan tiedon pohjalta.

Tiedot (relevantteja kysymyksiä ja vastauksia):
{knowledge}

Kysymys:
{question}
"""
    elif role == "IT":
        return f"""
Olet tehokas IT-tukihenkilö.
Vastaa ongelmaan asiantuntevasti alla olevan tiedon pohjalta.

Tiedot (relevantteja kysymyksiä ja vastauksia):
{knowledge}

Kysymys:
{question}
"""
    elif role == "SEC":
        return f"""
Olet tietoturva-asiantuntija.
Vastaa kysymykseen alla olevan tiedon pohjalta.

Tiedot (relevantteja kysymyksiä ja vastauksia):
{knowledge}

Kysymys:
{question}
"""