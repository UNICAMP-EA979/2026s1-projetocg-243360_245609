from collections import deque
 
import numpy as np
import sys
#sys.path.insert(0, r"C:\Users\rafae\2026-cg03-pbr-243360_245609\src")
import urenderer
from OpenGL import GL
from urenderer.node import Node
from urenderer.renderer.opengl import Material, Texture
 
NOME_DA_CENA = "universo"
 
def update_orbit(node: Node, deltaTime: float, time_since_start: float) -> None:
    """Faz o nó orbitar em torno de node.center no plano XZ."""
    center = node.center
    radius = node.orbit_radius
    speed  = node.orbit_speed
 
    angle = time_since_start * speed
    node.translation[0] = center[0] + radius * np.cos(angle)
    node.translation[2] = center[2] + radius * np.sin(angle)
    node.translation[1] = center[1]
 
    node.rotation[1] = np.degrees(angle) * 2
 
def update_orbit_tilted(node: Node, deltaTime: float, time_since_start: float) -> None:
    """Orbita em torno de node.center com inclinação no eixo Y+X."""
    center = node.center
    radius = node.orbit_radius
    speed  = node.orbit_speed
    tilt   = node.orbit_tilt  # inclinação em radianos

    angle = time_since_start * speed
    node.translation[0] = center[0] + radius * np.cos(angle)
    node.translation[1] = center[1] + radius * np.sin(angle) * np.sin(tilt)
    node.translation[2] = center[2] + radius * np.sin(angle) * np.cos(tilt)

    # Tumbling — rotação caótica do asteroide
    node.rotation[0] = np.degrees(angle) * 1.3
    node.rotation[1] = np.degrees(angle) * 2.0
    node.rotation[2] = np.degrees(angle) * 0.7
 
def update_pulse(node: Node, deltaTime: float, time_since_start: float) -> None:
    """Faz o nó pulsar de tamanho."""
    scale = 1.0 + 0.15 * np.sin(time_since_start * 2.0)
    node.scale = scale * np.ones(3)
 
if __name__ == "__main__":
    urenderer.utils.clear_workdir(NOME_DA_CENA)
    renderer = urenderer.renderer.OpenGLRenderer(1920, 1080)
    renderer.background_color = np.array([0.01, 0.01, 0.02, 1], np.float32)
    runtime = urenderer.application.Runtime(renderer, name=NOME_DA_CENA)
 
    renderer.ambient_color = np.array([0.05, 0.05, 0.08], dtype=np.float32)
 
    shader = urenderer.renderer.Shader("assets/vertex.vs", "assets/05-fragment.fs")
 
    # ── Texturas ──────────────────────────────────────────────────────────────
    whiteR  = Texture(255 * np.ones((1, 1),    np.uint8), GL.GL_RED, GL.GL_R8)
    blackR  = Texture(np.zeros((1, 1),         np.uint8), GL.GL_RED, GL.GL_R8)
    whiteRGB= Texture(255 * np.ones((1,1,3),   np.uint8), GL.GL_RGB, GL.GL_RGB)
 
    metalBaseColor = Texture.load_file(
        "assets/Metal048A_1K-JPG/Metal048A_1K-JPG_Color.jpg",
        srgb=True, drop_alpha=True)
    metalMetallic  = Texture.load_file(
        "assets/Metal048A_1K-JPG/Metal048A_1K-JPG_Metalness.jpg",
        drop_alpha=True)
    metalRoughness = Texture.load_file(
        "assets/Metal048A_1K-JPG/Metal048A_1K-JPG_Roughness.jpg",
        drop_alpha=True)
 
    rockBaseColor = Texture.load_file(
        "assets/Rock035_1K-JPG/Rock035_1K-JPG_Color.jpg",
        srgb=True, drop_alpha=True)
    rockRoughness = Texture.load_file(
        "assets/Rock035_1K-JPG/Rock035_1K-JPG_Roughness.jpg",
        drop_alpha=True)

    brickBaseColor = Texture.load_file(
        "assets/Bricks104_1K-JPG/Bricks104_1K-JPG_Color.jpg",
        srgb=True, drop_alpha=True)
    brickRoughness = Texture.load_file(
        "assets/Bricks104_1K-JPG/Bricks104_1K-JPG_Roughness.jpg",
        drop_alpha=True)
 
    # ── Materiais ─────────────────────────────────────────────────────────────
    matMetal = Material(shader)
    matMetal.set_texture(0, "baseColorTexture", metalBaseColor)
    matMetal.set_texture(1, "metallicTexture",  metalMetallic)
    matMetal.set_texture(2, "roughnessTexture", metalRoughness)
 
    roughMetallic = Texture(180 * np.ones((1,1), np.uint8), GL.GL_RED, GL.GL_R8)
    matRoughMetal = matMetal.clone()
    matRoughMetal.set_texture(2, "roughnessTexture", roughMetallic)
 
    matBrick = Material(shader)
    matBrick.set_texture(0, "baseColorTexture", brickBaseColor)
    matBrick.set_texture(1, "metallicTexture",  blackR)
    matBrick.set_texture(2, "roughnessTexture", brickRoughness)
    matBrick.set_uniform("tiling", 4.0)
 
    matPlastic = Material(shader)
    matPlastic.set_texture(0, "baseColorTexture", whiteRGB)
    matPlastic.set_texture(1, "metallicTexture",  blackR)
    matPlastic.set_texture(2, "roughnessTexture", whiteR)

    # Asteroide metálico (cubo)
    matAsteroidMetal = matMetal.clone()

    # Asteroide rochoso (triângulo)
    matAsteroidRock = Material(shader)
    matAsteroidRock.set_texture(0, "baseColorTexture", rockBaseColor)
    matAsteroidRock.set_texture(1, "metallicTexture",  blackR)
    matAsteroidRock.set_texture(2, "roughnessTexture", rockRoughness)
 
    # ── Geometria ─────────────────────────────────────────────────────────────
    sphere_mesh   = urenderer.geometry.mesh.get_mesh_sphere()
    cube_mesh     = urenderer.geometry.mesh.get_mesh_cube()
    triangle_mesh = urenderer.geometry.mesh.get_mesh_triangle()

    orbit_center = np.array([0.0, 0.0, -7.0])

    # Planeta central (pulsa)
    center_sphere = urenderer.node.Node()
    center_sphere.translation = np.array([0.0, 0.0, -7.0])
    center_sphere.render_data["mesh"]     = sphere_mesh
    center_sphere.render_data["material"] = matMetal
    center_sphere.callbacks = [update_pulse]
    runtime.scene.add_child(center_sphere)
 
    # Esferas que orbitam ao redor do planeta — todas de tijolo
    orbit_configs = [
        (matAsteroidRock, 2.5,  1.0,  0.0),
        (matBrick, 2.5,  1.0,  np.pi * 2/3),
        (matBrick, 2.5,  1.0,  np.pi * 4/3),
        (matBrick, 4.0,  0.6,  np.pi / 4),
        (matBrick, 4.0,  0.6,  np.pi * 5/4),
    ]
 
    for mat, radius, speed, phase in orbit_configs:
        s = urenderer.node.Node()
        s.translation = np.array([
            orbit_center[0] + radius * np.cos(phase),
            orbit_center[1],
            orbit_center[2] + radius * np.sin(phase),
        ])
        s.scale = 0.5 * np.ones(3)
        s.render_data["mesh"]     = sphere_mesh
        s.render_data["material"] = mat
        s.center       = orbit_center.copy()
        s.orbit_radius = radius
        s.orbit_speed  = speed
        s.callbacks = [update_orbit]
        runtime.scene.add_child(s)

    # ── Asteroide cúbico (metal) ───────────────────────────────────────────────
    asteroid_cube = urenderer.node.Node()
    asteroid_cube.translation = np.array([
        orbit_center[0] + 3.2,
        orbit_center[1],
        orbit_center[2],
    ])
    asteroid_cube.scale = np.array([0.35, 0.35, 0.35])
    asteroid_cube.render_data["mesh"]     = cube_mesh
    asteroid_cube.render_data["material"] = matAsteroidRock
    asteroid_cube.center       = orbit_center.copy()
    asteroid_cube.orbit_radius = 3.2
    asteroid_cube.orbit_speed  = 0.8
    asteroid_cube.orbit_tilt   = np.radians(25)
    asteroid_cube.callbacks = [update_orbit_tilted]
    runtime.scene.add_child(asteroid_cube)

    # ── Asteroide triangular (rocha) ───────────────────────────────────────────
    asteroid_tri = urenderer.node.Node()
    asteroid_tri.translation = np.array([
        orbit_center[0] + 3.8 * np.cos(np.pi),
        orbit_center[1],
        orbit_center[2] + 3.8 * np.sin(np.pi),
    ])
    asteroid_tri.scale = np.array([0.8, 0.8, 0.8])
    asteroid_tri.render_data["mesh"]     = triangle_mesh
    asteroid_tri.render_data["material"] = matBrick  
    asteroid_tri.center       = orbit_center.copy()
    asteroid_tri.orbit_radius = 3.8
    asteroid_tri.orbit_speed  = -0.55   # orbita no sentido contrário
    asteroid_tri.orbit_tilt   = np.radians(-35)
    asteroid_tri.callbacks = [update_orbit_tilted]
    runtime.scene.add_child(asteroid_tri)
 
    # ── Luzes ─────────────────────────────────────────────────────────────────
    # Luz central branca para iluminar todos os objetos
    light_center = urenderer.node.Light(urenderer.node.LightType.POINT)
    light_center.translation              = np.array([0.0, 0.0, -5.0])
    light_center.light_color              = np.array([1.0, 1.0, 1.0], np.float32)
    light_center.light_intensity          = 20.0
    light_center.light_reference_distance = 8.0
    runtime.scene.add_child(light_center)
 
    light_main = urenderer.node.Light(urenderer.node.LightType.DIRECTIONAL)
    light_main.rotation        = np.array([-135.0, -5.0, 0.0])
    light_main.light_color     = np.array([1.0, 1.0, 1.0], np.float32)
    light_main.light_intensity = 5.0
    runtime.scene.add_child(light_main)
 
    light_blue = urenderer.node.Light(urenderer.node.LightType.POINT)
    light_blue.translation              = np.array([-5.0, 2.0, -6.0])
    light_blue.light_color              = np.array([0.2, 0.4, 1.0], np.float32)
    light_blue.light_intensity          = 15.0
    light_blue.light_reference_distance = 6.0
    runtime.scene.add_child(light_blue)
 
    light_orange = urenderer.node.Light(urenderer.node.LightType.POINT)
    light_orange.translation              = np.array([5.0, 1.0, -6.0])
    light_orange.light_color              = np.array([1.0, 0.5, 0.1], np.float32)
    light_orange.light_intensity          = 15.0
    light_orange.light_reference_distance = 6.0
    runtime.scene.add_child(light_orange)
 
    light_mag = urenderer.node.Light(urenderer.node.LightType.POINT)
    light_mag.translation              = np.array([0.0, -3.0, -7.0])
    light_mag.light_color              = np.array([1.0, 0.0, 0.8], np.float32)
    light_mag.light_intensity          = 10.0
    light_mag.light_reference_distance = 5.0
    runtime.scene.add_child(light_mag)
 
    # ── Renderização ──────────────────────────────────────────────────────────
    video = True
    if video:
        runtime.loop(n=4000, capture=np.arange(0, 4000, 40, dtype=np.int32))
        urenderer.utils.image_to_video(NOME_DA_CENA, fps=30)
        urenderer.utils.clear_workdir(NOME_DA_CENA, image_only=True)
    else:
        runtime.loop(capture=[1])