#version 330 core

#include "light.glsl"
#include "fresnel.glsl"
#include "diffuse.glsl"
#include "specular.glsl"

#define MAX_LIGHT 10
#define PI 3.14159265359

// Adicione suporte para texturas com tiling

in vec3 worldPosition;
in vec3 worldNormal;
in vec2 uv;

uniform vec3 ambientColor;
uniform sampler2D baseColorTexture;
uniform sampler2D metallicTexture;
uniform sampler2D roughnessTexture;
uniform sampler2D skyboxTexture; 

uniform float tiling = 1.0;

out vec4 FragColor;

uniform Light lights[MAX_LIGHT];

void main()
{
    // Calcule a normal do fragmento
    vec3 worldNormalNormalized = normalize(gl_FrontFacing ? worldNormal : -worldNormal);

    // Calcule a direção de visualização (saindo do ponto)
    vec3 viewDirection = normalize(-worldPosition);

    // Calcule a uv com tiling
    vec2 uvTiling = uv * tiling;

    // Realize sampling das texturas para obter as propriedades da superfície
    vec3 baseColor = texture(baseColorTexture, uvTiling).rgb;
    float metallic = texture(metallicTexture, uvTiling).r;
    float roughness = max(texture(roughnessTexture, uvTiling).r, 0.05);

    vec3 color = vec3(0);

    //Cálculo da Luz Ambiente e Reflexão
    vec3 r = reflect(-viewDirection, worldNormalNormalized);
    
    // Converte o vetor de reflexão num mapeamento UV de 360 graus
    float u_env = atan(r.z, r.x) / (2.0 * PI) + 0.5;
    float v_env = asin(r.y) / PI + 0.5;
    vec2 envUV = vec2(u_env, v_env);

    // Lê a cor do Universo nesse ângulo
    vec3 reflectionColor = texture(skyboxTexture, envUV).rgb;

    // Aplica o Fresnel base para a reflexão
    vec3 F0_env = mix(vec3(0.04), baseColor, metallic);
    vec3 fresnel_env = F0_env + (1.0 - F0_env) * pow(1.0 - max(dot(worldNormalNormalized, viewDirection), 0.0), 5.0);

    // Componente base (escura para metais puros)
    vec3 ambientBase = baseColor * ambientColor * (1.0 - metallic);
    
    // Componente reflexiva 
    // Diminuímos a intensidade baseada na rugosidade (roughness) para imitar dispersão especular
    vec3 indirectSpecular = reflectionColor * fresnel_env * (1.0 - roughness);
    
    vec3 ambientLightContribution = ambientBase + indirectSpecular;
    for(int i = 0; i < MAX_LIGHT; i++)
    {
        Light light = lights[i];
        if(light.type == LIGHT_UNSET)
        {
            break;
        }

        //Calcule dados da luz 
        float attenuation = (light.type == 2) ? 
        pow(light.reference_distance / max(distance(light.position, worldPosition), light.reference_distance), 2.0) : 1.0;
        vec3 lightColor = light.color * light.intensity * attenuation;
        
        vec3 lightDirection = (light.type == 1) ? normalize(-light.direction) : normalize(light.position - worldPosition);
        
        //Calcule o half-angle
        vec3 halfAngle = normalize(lightDirection + viewDirection);
        
        //Calcule as refletância de fresnel, difusa e especular
        vec3 fresnel = fresnelReflectance(baseColor, metallic, halfAngle, lightDirection);
        vec3 diffuse = (1.0 - fresnel) * (baseColor / PI) * (1.0 - metallic);
        vec3 specular = specularReflectance(fresnel, worldNormalNormalized, halfAngle, viewDirection, lightDirection, roughness);

        vec3 reflectance = diffuse + specular;
        vec3 lightContribution = reflectance * lightColor * max(dot(worldNormalNormalized, lightDirection), 0.0);
        color += lightContribution;
    }

    FragColor = vec4(ambientLightContribution + color, 1.0);
}