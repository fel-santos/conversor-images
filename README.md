Conversor de Imagens com Tkinter
Fala, galera! 👋

Este aqui é um app de desktop super simples e fácil de usar, feito para te ajudar a dar um trato nas suas imagens. Com ele, você pode converter para vários formatos, mudar o tamanho, ajustar a qualidade e, o melhor de tudo, ver como tudo vai ficar antes de salvar.

O que ele faz?
Este app foi feito para facilitar a sua vida! Dá uma olhada em tudo que ele consegue fazer:

Converte entre vários formatos: De JPEG a PNG, BMP, WEBP, TIFF e até ICO. É só escolher o que você precisa.

Muda o tamanho: Quer deixar a imagem maior ou menor? É só digitar a largura e a altura que você quer.

Ajusta a qualidade: Com um controle deslizante, você consegue afinar a qualidade de saída, com uma precisão de uma casa decimal.

Pré-visualização instantânea: Não precisa adivinhar! Quando você abre uma imagem, ela já aparece na tela para você ver tudo.

Salva com nome inteligente: A janela para salvar já vem com o nome original da imagem, mas com a nova extensão. É só clicar e pronto!

E tem um ícone: A janela do aplicativo tem um ícone personalizado para ficar com uma cara mais descontraída.

Bora instalar?
Pra começar a usar, você só precisa do Python instalado. Depois, é só rodar um comando para instalar a biblioteca que o app usa. Bem simples!

Abra seu terminal e digite:

pip install Pillow

Pra rodar é fácil!
Pegue o código: Clone o projeto ou baixe os arquivos conversor_imagem.py e icone.ico.

Ligue o motor: No seu terminal, vá até a pasta do projeto e use este comando para ligar o app:

python conversor_imagem.py

Quer um .exe? (É opcional!)
Pra deixar o app ainda mais prático, você pode transformá-lo num arquivo executável (.exe). Assim, qualquer pessoa pode usar, mesmo sem ter o Python instalado. O segredo é o PyInstaller.

Instale o PyInstaller: Se ele ainda não está na sua máquina, é só rodar:

pip install pyinstaller

Faça a mágica acontecer: Na pasta do projeto, use o comando para gerar o executável. Atenção: o --add-data é super importante pra garantir que o ícone vá junto!

Se você usa Windows:

pyinstaller --onefile --noconsole --add-data "icone.ico;." conversor_imagem.py

Se for Linux ou macOS:

pyinstaller --onefile --noconsole --add-data "icone.ico:." conversor_imagem.py

Encontre o resultado: O arquivo .exe vai estar lá na pasta dist/, prontinho para ser usado.

Uma Dica sobre o Ícone
Fique de olho! O arquivo icone.ico tem que estar na mesma pasta do conversor_imagem.py pra tudo funcionar direitinho, tanto pra rodar o script quanto pra criar o executável.
