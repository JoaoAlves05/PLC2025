import re
import sys

def markdown_to_html(markdown):
    html = [] # Lista para guardar linhas HTML
    lines = markdown.split('\n') # Dividir o texto em linhas
    in_list = False

    for line in lines:
        line = line.strip()

        # Cabeçalhos
        if re.match(r'### ', line):
            html.append(f"<h3>{line[4:]}</h3>")
        elif re.match(r'## ', line):
            html.append(f"<h2>{line[3:]}</h2>")
        elif re.match(r'# ', line):
            html.append(f"<h1>{line[2:]}</h1>")

        # Lista numerada
        elif re.match(r'\d+\.\s', line):
            if not in_list:
                html.append("<ol>")
                in_list = True
            item = re.sub(r'^\d+\.\s+', '', line)
            html.append(f"<li>{item}</li>")
        else:
            if in_list:
                html.append("</ol>")
                in_list = False

            line = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', line)  # negrito
            line = re.sub(r'\*(.*?)\*', r'<i>\1</i>', line)      # italico
            line = re.sub(r'!\[(.*?)\]\((.*?)\)', r'<img src="\2" alt="\1"/>', line)  # imagem
            line = re.sub(r'\[(.*?)\]\((.*?)\)', r'<a href="\2">\1</a>', line)        # link

            if line:
                html.append(f"<p>{line}</p>")

    if in_list:
        html.append("</ol>")

    return '\n'.join(html)


# --- Ler do stdin ---
if __name__ == "__main__":
    html_output = markdown_to_html(sys.stdin.read())
    print(html_output)

