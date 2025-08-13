import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk, ImageEnhance
import os
import sys

# Função para resolver o problema de caminho de arquivo para executáveis
def resource_path(relative_path):
    """Obtém o caminho absoluto do recurso, para funcionar no modo dev e no PyInstaller"""
    try:
        # PyInstaller cria uma pasta temporária e armazena o caminho em _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)

class ImageConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Conversor de Imagens")
        
        # --- AQUI ESTÁ A MUDANÇA PARA O ÍCONE ---
        # Usa a nova função para encontrar o ícone
        try:
            icon_path = resource_path('icone.ico')
            self.root.iconbitmap(icon_path)
        except tk.TclError:
            print("Aviso: O arquivo icone.ico não foi encontrado. O ícone padrão será usado.")
        
        self.root.geometry("800x450")
        self.root.resizable(False, False)

        self.image_path = None
        self.original_image = None
        self.preview_photo = None

        # Configurar o estilo da janela
        style = ttk.Style()
        style.configure("TFrame", background="#f0f0f0")
        style.configure("TLabel", background="#f0f0f0", font=("Helvetica", 10))
        style.configure("TButton", font=("Helvetica", 10, "bold"))
        style.configure("TCombobox", font=("Helvetica", 10))

        # --- Layout Principal: Dividir em duas colunas ---
        self.main_frame = ttk.Frame(root, padding="15")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Frame da Esquerda (Controles)
        self.control_frame = ttk.Frame(self.main_frame)
        self.control_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 15))

        # Frame da Direita (Pré-visualização)
        self.preview_frame = ttk.Frame(self.main_frame)
        self.preview_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        self.preview_label = ttk.Label(self.preview_frame, text="Pré-visualização da Imagem", anchor="center", font=("Helvetica", 12))
        self.preview_label.pack(fill=tk.BOTH, expand=True)
        
        # --- Seção 1: Seleção de Imagem (no frame de controle) ---
        selection_frame = ttk.LabelFrame(self.control_frame, text="1. Seleção de Imagem", padding="10")
        selection_frame.pack(fill=tk.X, pady=(0, 10))

        self.button_select = ttk.Button(selection_frame, text="Abrir Imagem", command=self.open_image)
        self.button_select.pack(fill=tk.X, pady=(0, 5))

        self.image_path_label = ttk.Label(selection_frame, text="Nenhuma imagem selecionada.", wraplength=350)
        self.image_path_label.pack(anchor=tk.W, pady=(0, 5))
        
        # --- Seção 2: Opções de Conversão (no frame de controle) ---
        options_frame = ttk.LabelFrame(self.control_frame, text="2. Opções de Conversão", padding="10")
        options_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Formato de saída
        format_frame = ttk.Frame(options_frame)
        format_frame.pack(fill=tk.X, pady=(0, 10))
        ttk.Label(format_frame, text="Formato:").pack(side=tk.LEFT, padx=(0, 5))
        
        self.formats = ["JPEG", "PNG", "BMP", "WEBP", "TIFF", "ICO"]
        self.format_var = tk.StringVar(format_frame)
        self.format_var.set("JPEG")
        self.format_menu = ttk.Combobox(format_frame, textvariable=self.format_var, values=self.formats, state="readonly")
        self.format_menu.pack(side=tk.LEFT, expand=True, fill=tk.X)
        
        # Resolução
        resolution_frame = ttk.Frame(options_frame)
        resolution_frame.pack(fill=tk.X, pady=(0, 10))
        ttk.Label(resolution_frame, text="Resolução (pixels):").pack(side=tk.LEFT, padx=(0, 5))
        
        self.width_var = tk.StringVar(resolution_frame)
        self.height_var = tk.StringVar(resolution_frame)
        
        self.width_entry = ttk.Entry(resolution_frame, textvariable=self.width_var, width=10)
        self.width_entry.pack(side=tk.LEFT, expand=True, fill=tk.X)
        ttk.Label(resolution_frame, text="x").pack(side=tk.LEFT, padx=5)
        self.height_entry = ttk.Entry(resolution_frame, textvariable=self.height_var, width=10)
        self.height_entry.pack(side=tk.LEFT, expand=True, fill=tk.X)

        # Qualidade (com valor flutuante para 1 casa decimal)
        quality_frame = ttk.Frame(options_frame)
        quality_frame.pack(fill=tk.X)
        ttk.Label(quality_frame, text="Qualidade:").pack(side=tk.LEFT, padx=(0, 5))
        
        self.quality_var = tk.DoubleVar(quality_frame)
        self.quality_var.set(95.0)  # Qualidade padrão com 1 casa decimal
        
        self.quality_scale = ttk.Scale(quality_frame, from_=1.0, to=100.0, orient=tk.HORIZONTAL, variable=self.quality_var, command=self.update_quality_label)
        self.quality_scale.pack(side=tk.LEFT, expand=True, fill=tk.X)
        
        self.quality_label = ttk.Label(quality_frame, text="95.0")
        self.quality_label.pack(side=tk.LEFT, padx=(5, 0))

        # --- Seção 3: Conversão (no frame de controle) ---
        convert_frame = ttk.LabelFrame(self.control_frame, text="3. Ação", padding="10")
        convert_frame.pack(fill=tk.X)

        self.button_convert = ttk.Button(convert_frame, text="Converter e Salvar", command=self.convert_image, state=tk.DISABLED)
        self.button_convert.pack(fill=tk.X)

    def update_quality_label(self, value):
        """Atualiza o rótulo de qualidade com o valor do slider formatado."""
        self.quality_label.config(text=f"{float(value):.1f}")
        
    def open_image(self):
        """Abre a caixa de diálogo para selecionar um arquivo de imagem e mostra a pré-visualização."""
        file_types = [
            ("Arquivos de Imagem", "*.jpg *.jpeg *.png *.bmp *.webp *.tiff *.ico"),
            ("Todos os Arquivos", "*.*")
        ]
        self.image_path = filedialog.askopenfilename(filetypes=file_types)
        
        if self.image_path:
            try:
                self.original_image = Image.open(self.image_path)
                self.image_path_label.config(text=f"Imagem selecionada: {os.path.basename(self.image_path)}", wraplength=350)
                
                self.width_var.set(self.original_image.width)
                self.height_var.set(self.original_image.height)
                
                self.show_preview(self.original_image)
                
                self.button_convert.config(state=tk.NORMAL)
            except Exception as e:
                messagebox.showerror("Erro", f"Não foi possível abrir a imagem: {e}")
                self.image_path = None
                self.original_image = None
                self.image_path_label.config(text="Nenhuma imagem selecionada.")
                self.button_convert.config(state=tk.DISABLED)
                self.preview_label.config(image="")

    def show_preview(self, pil_image):
        """Exibe a imagem no espaço de pré-visualização."""
        max_size = (350, 350)
        temp_image = pil_image.copy()
        temp_image.thumbnail(max_size, Image.LANCZOS)
        
        self.preview_photo = ImageTk.PhotoImage(temp_image)
        self.preview_label.config(image=self.preview_photo, text="")

    def convert_image(self):
        """Converte e salva a imagem no formato, resolução e qualidade escolhidos."""
        if not self.original_image:
            messagebox.showwarning("Aviso", "Por favor, selecione uma imagem primeiro.")
            return

        output_format = self.format_var.get().lower()
        quality_level = int(self.quality_var.get())
        
        try:
            new_width = int(self.width_var.get())
            new_height = int(self.height_var.get())
            if new_width <= 0 or new_height <= 0:
                raise ValueError("Dimensões inválidas")
        except ValueError:
            messagebox.showerror("Erro de Resolução", "Por favor, insira valores numéricos válidos e maiores que zero para a largura e altura.")
            return

        processed_image = self.original_image.copy()
        processed_image = processed_image.resize((new_width, new_height), Image.LANCZOS)
        
        enhancer = ImageEnhance.Sharpness(processed_image)
        processed_image = enhancer.enhance(1.2)
        
        base_name = os.path.splitext(os.path.basename(self.image_path))[0]
        default_file_name = f"{base_name}.{output_format}"

        save_file_path = filedialog.asksaveasfilename(
            defaultextension=f".{output_format}",
            filetypes=[(f"Arquivos {output_format.upper()}", f"*.{output_format}")],
            initialfile=default_file_name
        )

        if save_file_path:
            try:
                if output_format == "jpeg" and processed_image.mode == 'RGBA':
                    rgb_image = Image.new('RGB', processed_image.size, (255, 255, 255))
                    rgb_image.paste(processed_image, mask=processed_image.split()[3])
                    rgb_image.save(save_file_path, quality=quality_level)
                else:
                    if output_format == "ico":
                        processed_image.save(save_file_path)
                    else:
                        processed_image.save(save_file_path, format=output_format.upper(), quality=quality_level)
                
                messagebox.showinfo("Sucesso", f"Imagem convertida e salva em:\n{save_file_path}")
            except Exception as e:
                messagebox.showerror("Erro", f"Não foi possível converter a imagem: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageConverterApp(root)
    root.mainloop()
