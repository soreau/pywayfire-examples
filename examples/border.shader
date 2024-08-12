#version 300 es
@builtin_ext@
@builtin@

precision mediump float;

uniform sampler2D in_tex;
out vec4 out_color;
in mediump vec2 uvpos;

void main()
{
    vec4 c = get_pixel(uvpos);
    ivec2 size = textureSize(in_tex, 0);
    vec2 texelSize = 2.0 / vec2(size);
    if (uvpos.x <= texelSize.x || uvpos.y <= texelSize.y ||
        uvpos.x >= 1.0 - texelSize.x || uvpos.y >= 1.0 - texelSize.y)
    {
        c.r = 0.9216;
        c.g = 0.8588;
        c.b = 0.6980;
        c.a = 1.0;
    }
    out_color = c;
}

