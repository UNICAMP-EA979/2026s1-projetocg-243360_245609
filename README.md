[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-2e0aaae1b6195c2367325f4f02e2d04e9abb55f0b24a779b69b11b9e10269abc.svg)](https://classroom.github.com/online_ide?assignment_repo_id=24207996&assignment_repo_type=AssignmentRepo)
# Projeto de CG - Cena

Vamos utilizar o renderizador implementado nas tarefas anteriores para renderizar uma cena.

Sugerimos que comecem o projeto analisando o arquivo `atividade.py`. Ele tem um exemplo básico de cena utilizando texturas, geometria importada e outros recursos do renderizador. Este é apenas um exemplo simples mostrando recursos que você pode utilizar para preparar a cena. Esperamos que o projeto entregue seja melhor em composição e qualidade gráfica.

Também sugerimos que leiam inteiramente este documento antes de iniciar o projeto, a sua proposta de cena pode mudar caso decidam implementar um item opcional (mas vocês também podem decidir isso depois).

## Formato de entrega

Vocês devem entregar neste Projeto:

- Descrição de cena: descrição de cena que implementaram (no final deste documento).
- Código: código Python utilizado para implementar a cena. O ponto de entrada da cena deve ser `atividade.py`
- Assets: todo shader, modelo, textura e outros utilizado para implementar a cena. Devem estar na pasta `assets`
- Lista de Assets: lista de todos os assets baixados da internet (no final deste documento).
- Cena final renderizada: podendo ser tanto uma imagem quanto um vídeo.

## Tarefas

- Descrevam a cena que desejam implementar. 
  - Encontrem imagens e vídeos de referência.
  - Indiquem quais objetos estarão na cena.
  - Indiquem o resultado visual esperado. Existe algum conceito ou sentimento que querem passar com essa imagem/vídeo?
  - Sejam criativos! Vocês podem querer recriar alguma cena fictícia ou lugar do mundo real, fazer uma composição surreal, testar algum efeito ou fazer uma simulação de algum fenômeno físico.
- Copiem arquivos implementados anteriormente;
  - Copiem todo a pasta `src` da última atividade de CG
  - Copiem os shaders finais `vertex.vs` e `05-fragment.fs` para a pasta `assets`. Eles podem ser utilizados como base para implementar a renderização da cena de vocês, que pode utilizar diferentes shaders para cada objeto.
- Criem a geometria de cena.
  - Para isso, você pode utilizar tanto as primitivas que temos definidas (cubo, esfera, triângulo), quanto criar uma cena externamente e importar.
  - A cena pode utilizar assets encontrados na internet, desde que indicadas as fontes.
  - Para criar uma cena externamente, você pode utilizar programas de edição como o Blender, tanto utilizando modelos prontos quanto modelando eles. O programa deve suportar salvar o arquivo em GLTF (`.glb`), ou você pode convertê-lo de alguma forma. Existe uma função `urenderer.geometry.mesh.load_glb` que carrega um arquivo GLTF para o nosso grafo de cena.
- Determinem materiais para a cena;
  - Vocês podem, encontrar materiais para utilizar online (ex. https://ambientcg.com/list?type=atlas,material,decal)
  - Vocês também podem criar materiais.
- (Opcional): animem a cena.
  - O arquivo de exemplo contém formas de animar objetos, como alterar a posição, rotação e escala utilizando uma função do tempo, ou simulando numericamente uma equação diferencial.
- (Opcional): realizem alterações na renderização para alcançar algum resultado desejado:
  - Melhorias no sistema de sombreamento: vocês podem implementar alterações no sombreamento, como [IBL](https://learnopengl.com/PBR/IBL/Diffuse-irradiance) (_image base lighting_) para renderizar melhor materiais metálicos, adicionar [sombras](https://learnopengl.com/Advanced-Lighting/Shadows/Shadow-Mapping), utilizar uma refletância especular melhor como a [GGX](https://learnopengl.com/PBR/Lighting) ou implementar [normal mapping](https://learnopengl.com/Advanced-Lighting/Normal-Mapping) para aparência mais realista de materiais tridimensionais.
  - [Pós-processamento](https://learnopengl.com/Advanced-OpenGL/Framebuffers): efeitos implementados na parte de Processamento de Imagem podem ser bons pós-processamentos para CG, efeitos aplicados após renderizar um frame.
  - Modelos de sombreamento não realista: trabalhamos na disciplina principalmente sombreamento realista com PBR, mas existem muitas formas de realizar sombreamentos não realistas e estilizados. A complexidade deles varia, e podem trazer visuais muito interessantes.

## Avaliação

O projeto será avaliado segundo:

- Complexidade da composição: a geometria, seu posicionamento (layout) e texturas utilizadas.
- Qualidade gráfica: como a composição foi renderizada, se apresenta problemas de iluminação ou artefatos.
- Estética: como a composição e renderização se relacionam com a proposta apresentada.
- Técnica: o código implementado, como está organizado e quais conceitos aplica.


# Entregas Textuais

## Descrição da cena

Descreva a cena que implementaram:

`Fizemos um sistema planetário com planetas e asteroides, com asteroides triangulares e cúbicos. Terá 3 planetas e 2 asteroides. Os 2 asteroides e 2 planetas orbitaram o planeta principal. O planeta principal é metálico, e os outros dois são feitos de tijolos. O asteroide triangular é feito de metal e o cúbico é feito de rocha. Todos orbitam ao redor do planeta principal. Os asteroides orbitam circularmente em torno do eixo z e os planetas em torno do eixo y. O planeta principal se move para frente e para trás (translação no eixo z). Os assets usados são cores e texturas de tijolos, metal e rocha. O asset de tijolo consiste na seguinte cor :![Bricks104 Color](assets/Bricks104_1K-JPG/Bricks104_1K-JPG_Color.jpg) e na seguinte textura: ![Bricks104 Roughness](assets/Bricks104_1K-JPG/Bricks104_1K-JPG_Roughness.jpg). O de metal consiste na seguinte cor: ![Metal048 Color](assets/Metal048A_1K-JPG/Metal048A_1K-JPG_Color.jpg), na seguinte característica metálica: ![Metal048 Metalness](assets/Metal048A_1K-JPG/Metal048A_1K-JPG_Metalness.jpg) e na seguinte textura: ![Metal048 Roughness](assets/Metal048A_1K-JPG/Metal048A_1K-JPG_Roughness.jpg). O de rocha consiste na seguinte cor: ![Rock035 Color](assets/Rock035_1K-JPG/Rock035_1K-JPG_Color.jpg) e na seguinte textura: ![Rock035 Roughness](assets/Rock035_1K-JPG/Rock035_1K-JPG_Roughness.jpg)Além disso, implementamos o item opcional de melhorias na renderização, adicionando Image-Based Lighting (IBL) através de Mapeamento de Reflexão Equiretangular. Alteramos a matemática do Fragment Shader para calcular vetores de reflexão física a partir da câmera e da normal da superfície, combinando-os com a Aproximação de Schlick para a Equação de Fresnel. Isso nos permitiu criar um efeito de espelhamento avançado, fazendo com que o planeta principal metálico atue como um espelho e reflita a imagem panorâmica 360° de uma galáxia.`

(Dica: para incluir imagens, utilize ![](Caminho da imagem))

## Assets utilizados

Para todo asset que tiver baixado da internet, coloque a referência dele (segundo eterminado por sua licensa):
`(Os mesmos que usamos na CG03)`
- `Bricks104_1K-JPG`: `CC0` (`https://polyhaven.com/a/bricks`) 
- `Metal048A_1K-JPG`: `CC0` (`https://polyhaven.com/a/metal`)
- `Rock035_1K-JPG`: `CC0` (`https://polyhaven.com/a/rock`)
- `Blue-universe-956981.jpg`: `Pexels License — Felix Mittermeier` (`https://www.pexels.com/photo/blue-universe-956981/`)
