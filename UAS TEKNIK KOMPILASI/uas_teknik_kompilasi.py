import re

class WhileCompiler:
    def __init__(self, source_code):
        self.source_code = source_code
        self.label_counter = 1
        self.symbol_table = {"x": "int", "y": "int"} # Simulasi tabel simbol untuk cek semantik

    def new_label(self):
        lbl = f"L{self.label_counter}"
        self.label_counter += 1
        return lbl

    # 1. ANALISIS LEKSIKAL (Tokenisasi)
    def lexical_analysis(self):
        # Memisahkan karakter khusus agar mudah di-tokenisasi
        spaced_code = re.sub(r'([(){}=><!+/*-])', r' \1 ', self.source_code)
        tokens = spaced_code.split()
        return tokens

    # 2 & 3. ANALISIS SINTAKSIS (AST) & SEMANTIK
    def syntax_and_semantic_analysis(self, tokens):
        # Validasi struktur dasar 'while'
        if tokens[0] != 'while' or '(' not in tokens or ')' not in tokens or '{' not in tokens or '}' not in tokens:
            raise SyntaxError("🚨 Error Sintaks: Struktur 'while' tidak valid.")

        # Ekstrak Kondisi (di dalam kurung)
        idx_open_p = tokens.index('(')
        idx_close_p = tokens.index(')')
        condition_tokens = tokens[idx_open_p + 1 : idx_close_p]
        condition_str = " ".join(condition_tokens)

        # Analisis Semantik Sederhana pada Kondisi
        for token in condition_tokens:
            if token.isalpha() and token not in self.symbol_table:
                raise NameError(f"🚨 Error Semantik: Variabel '{token}' belum dideklarasikan!")

        # Ekstrak Isi/Body (di dalam kurung kurawal)
        idx_open_b = tokens.index('{')
        idx_close_b = tokens.index('}')
        body_tokens = tokens[idx_open_b + 1 : idx_close_b]
        body_str = " ".join(body_tokens)

        # Representasi AST Sederhana dalam bentuk Dictionary
        ast = {
            "node_type": "WhileLoop",
            "condition": condition_str,
            "body": body_str
        }
        return ast

    # 4. GENERASI KODE ANTARA (Three-Address Code / TAC)
    def generate_tac(self, ast):
        lbl_start = self.new_label()
        lbl_body = self.new_label()
        lbl_end = self.new_label()

        tac = []
        tac.append(f"{lbl_start}:")
        tac.append(f"if {ast['condition']} goto {lbl_body}")
        tac.append(f"goto {lbl_end}")
        tac.append(f"{lbl_body}:")
        tac.append(f"  {ast['body']}")
        tac.append(f"goto {lbl_start}")
        tac.append(f"{lbl_end}:")
        
        return "\n".join(tac)

# --- CARA MENJALANKAN SIMULASI ---
if __name__ == "__main__":
    # Input kode sumber tiruan yang akan dikompilasi
    source_input = "while ( x < 10 ) { x = x + 1 }"
    
    print("="*50)
    print("KODE SUMBER INPUT:")
    print(f"  {source_input}")
    print("="*50)

    compiler = WhileCompiler(source_input)

    try:
        # Tahap 1: Leksikal
        tokens = compiler.lexical_analysis()
        print("\n1. [HASIL ANALISIS LEKSIKAL]")
        print(f"   Tokens: {tokens}")

        # Tahap 2 & 3: Sintaksis & Semantik
        ast = compiler.syntax_and_semantic_analysis(tokens)
        print("\n2 & 3. [HASIL ANALISIS SINTAKSIS (AST) & SEMANTIK]")
        print(f"   AST Node: {ast}")
        print("   Status Semantik: Valid (Semua variabel terdaftar)")

        # Tahap 4: TAC Generator
        tac_code = compiler.generate_tac(ast)
        print("\n4. [GENERASI THREE-ADDRESS CODE (TAC)]")
        print(tac_code)
        print("="*50)

    except Exception as e:
        print(str(e))