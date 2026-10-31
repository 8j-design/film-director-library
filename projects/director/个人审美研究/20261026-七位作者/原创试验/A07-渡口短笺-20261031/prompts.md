# 《渡口短笺》实际提示词与模式

2026-10-31，内置image_gen，transparent_background=false。V1无图像输入；V2编辑原创V1；V3编辑原创V2；V4仅以原创V3保持身份、服装与地点并另做近景。没有第三方原帧输入。输出为四张静态图，不能当连续动画。

## V1

Use case: stylized-concept. Original artwork for a private filmmaking study, one finished cinematic keyframe, landscape 16:9. A clearly adult woman in her late twenties with a short dark auburn bob, small round silver earrings, a moss green scarf and a simple charcoal raincoat waits beside a small riverside ferry shelter after rain at night. She notices a friend behind the camera and starts a restrained playful greeting: her right hand raises a folded pale ferry ticket near her mouth, momentarily covering the lower lip, while her eyes meet the camera; her left hand lightly holds the coat closed at the waist. Show her from knees upward, enough environment to understand the shelter, rail and wet pavement, human hands with clear fingers and a believable wrist/ticket grip. Wind pushes the bob and scarf gently in the same direction. Carefully crafted stylized 3D character and environment, rounded but anatomically credible face, tactile matte fabric, no photoreal live-action look, no flat diagram. Cool blue grey night, a modest warm shelter light softly illuminates the face, distant ferry terminal lights become a few restrained out-of-focus discs; the face and ticket hand are the focal plane, environment still legible. Asymmetric natural composition, thoughtful everyday mood. Original character and location, no reference-image pixels, no recognizable existing character, no logos, no writing, no watermark. This is one keyframe, no panel layout, no labels, no cinematic letterbox.

## V2

Edit target: the supplied original ferry-shelter keyframe. Produce V2 of this artwork. Keep the exact adult character identity, auburn bob length, green scarf, charcoal coat, ticket near mouth, hand positions, camera framing, ferry shelter, river, boat, rail, wet ground, and warm/cool light arrangement. Correct two observed problems: (1) The current image reads too much like a live-action fashion photograph. Convert the entire character and environment into a clearly crafted stylized 3D animated-film render: softly simplified facial planes, slightly enlarged expressive eyes, sculpted grouped hair clumps, clean deliberate facial shapes, soft skin shading without photographic pores, simplified tactile fabrics and stylized architectural shapes. Maintain an adult late-twenties appearance and natural anatomy; avoid doll-like plastic gloss or flat anime illustration. (2) Unify the breeze: both hair tips and scarf fringe should trail gently toward image-right; keep face and eyes clear, without covering both eyes. Preserve the restrained everyday mood and legible shelter/river, with sparse distant bokeh. Do not add objects, makeup, labels, panel divisions, logos or watermarks. The ticket is plain pale folded paper without writing. This is a revision of one keyframe, not a diagram and not a new composition.

## V3

Edit target: the supplied stylized 3D ferry shelter artwork, make V3. Correct ONLY the scarf's silhouette: its large triangular windblown tail currently competes with the face and ticket. Shorten that visible flying tail by roughly half and lower its arc so it hangs in a gentle curved taper, softly trailing toward image-right at the lower chest. Keep the moss-green color, realistic thickness, fringe, and continuous connection around the neck; avoid turning it into a separate flat ribbon. Leave absolutely everything else as close as possible: same adult face and eye size, auburn hair, expression, ticket and hand grip, left hand, coat, body pose, framing, face lighting, matte stylized 3D rendering, ferry shelter architecture, boat, rail, rainy pavement, bokeh and color balance. No new objects or text. The intended improvement is a calmer visual hierarchy with the eyes and small ticket gesture dominant. One finished landscape keyframe, no diagrams or labels.

## V4

Use the supplied V3 original artwork as an identity, wardrobe and location reference. Make a revised cinematic keyframe V4 addressing the observed problem that the current greeting feels like distant fashion posing. Move the camera into a close shoulder-up view at the same ferry shelter and same time. Preserve exactly the same adult late-twenties woman, auburn bob, sculpted stylized 3D face, eye color, round silver earrings, green scarf and charcoal coat. She leans a little toward the familiar person behind the camera, with a small spontaneous open smile, and extends her RIGHT hand holding the same plain folded ferry ticket toward the lens as a playful invitation to join her. The ticket and right fingertips occupy the near foreground, softly out of focus and partially crossing the lower edge of her cheek, while her eyes are sharply readable and meet the lens. Maintain believable forearm-wrist connection and thumb/index-finger ticket grip; no extra hands or fingers. Keep warm shelter light on the hair rim, cool blue river ambience and sparse round bokeh, matte stylized 3D rather than live-action photography. A portion of the shelter frame and river remain recognizable in the background. Do not include source-video characters, text, logos, panel layout or watermarks. One horizontal finished keyframe; this is a new shot in the same original scene, not an animation or morph.

## 文件和实际验收

- V1-渡口短笺.png：初稿；实际看图后才请求V2。
- V2-渡口短笺.png：CG造型增强、围巾过大；实际看图后请求V3。
- V3-渡口短笺.png：围巾收短；回第6集原参考后，发现互动距离问题，另做V4。
- V4-近景递笺.png：新镜头；闭口笑/下脸无遮挡与请求有差异，手部虚焦难验。

完整研究与失败见任务正文《A07-渡口短笺四版原创与回原作检验-20261031.md》。提示词中的要求不是实际已实现的证据。
