# 数字三维对照补充：《Sprite Fright》完整官方成片与六份制作正文

2026-10-25。此任务接续《Pas de deux》，增加有角色、道具、环境、动画、镜头及制作协作的数字三维案例。已取得一份完整公开成片供主控实际解码；本子agent不启动Blender，不代报看图／看片／实听。本报告中制作方法是创作者正文所述，成片比较问题仍待实际观看后回答。

## 1. 已取得的一部成片

**《Sprite Fright - Open Movie by Blender Studio》720p**，来自Blender官方PeerTube的Blender账号公开条目。稳定观看入口：[官方成片](https://video.blender.org/videos/watch/a69d68a5-a0e0-4a80-9d66-49f093c97aaf)；[公开API](https://video.blender.org/api/v1/videos/a69d68a5-a0e0-4a80-9d66-49f093c97aaf) 明确 `downloadEnabled:true`，本次仅请求其列出的 [720p直接下载](https://video.blender.org/download/web-videos/a69d68a5-a0e0-4a80-9d66-49f093c97aaf-720.mp4)。无登录、Cookie、DRM、下载器安装或权限扩大。

- 本地：`reference_media/sprite_fright_official_720p.mp4`。
- 字节数：**102,392,846**，与API对应文件的 `size` 完全一致。
- SHA-256：`7cfc8b8c6eeb19685048a289aca208a01356f5082b470fb9f4d933fe4b2087ef`。
- 官方条目时长630秒，标注原始发布时间为2021-10-28T22:00:00Z；PeerTube发布时间为2021-10-31T01:44:46.154Z。二者是该站字段，不据此重新判定影片历史首映日期。
- [官方服务器probe](https://video.blender.org/api/v1/videos/a69d68a5-a0e0-4a80-9d66-49f093c97aaf/metadata/613510)：视频H.264 High、1718×720、24/1fps、**15116帧／629.833333秒**；AAC LC、双声道、44100Hz，音频629.88771秒；容器629.888秒。条目的630秒是取整，不能强写成精确630秒。
- 像素宽高比记录 `18383:18368`，显示宽高比 `160:67`，不能拉伸成16:9。1718×720是可见图像尺寸，码流记录的coded width为1728不代表应加一条可见画边。色域／传递函数字段为unknown，不自行补写“已经完成Rec.709／显示校准”。

上述流规格为**官方服务器元数据**，不是本子agent对下载文件作的本地逐帧解码。下载完成与尺寸匹配支持传输完整；尚不能保证每一帧无误、声音完整、正常速度流畅或音画同步。主控的本地解码与实际观看需另记。

本地回执：`sprite_fright_api.local.json`（原API全文）、`sprite_fright_download_manifest.local.json`（选档、HTTP响应、原URL、字节及哈希）、`sprite_fright_server_probe.local.json`（服务器probe）。均在 `reference_media/`，与原片一起仅本地参考，不上传归库。本次只下载这一个成片版本，没有另取1080p或同片多版本。

许可边界：这个PeerTube成片条目的 `licence` 实际为Unknown；官方下载开放与可合法本地研究可确认，但不据此宣称该文件已逐项核成CC-BY。Blender Studio的 [通用remixing说明](https://studio.blender.org/remixing/) 说通常CC-BY且每资产另有标注，这是通则，不自动填补此条目缺失字段。本轮不再发布原片，也不从demo场景许可替成片下结论。

### 另定位但未下载的《Spring》

[官方成片](https://video.blender.org/videos/watch/3d95fb3d-c866-42c8-9db1-fe82f48ccb95)／[公开API](https://video.blender.org/api/v1/videos/3d95fb3d-c866-42c8-9db1-fe82f48ccb95) 已实际读取：464秒，downloadEnabled为true，条目许可标签Attribution–Share Alike（此字段未指定版本）。有 [360p直接文件](https://video.blender.org/download/web-videos/3d95fb3d-c866-42c8-9db1-fe82f48ccb95-360.mp4) 858×360、38,025,811字节，以及720p等档。**只定位，不下载、不看图、不研究其连续剧情**。当前先把《Sprite Fright》一部从资料推进到实际成片比较。

## 2. 访问方式与正文范围

本轮网页工具对部分Blender页面报402，普通匿名HTTP对Studio及主站若干页报403；没有把这些误写成订阅付费要求，也没有绕登录。官方PeerTube公开API、下载地址和download.blender.org目录均普通HTTP 200可读。

以下六篇的正文实际通过网页检索返回的官方页面长文本读取，**不是只读标题或Style Guide索引**。长文本可覆盖所列正文段落，但本子agent没有下载其页面内的受订阅视频／工程，也没有实际view_image观察文中图片；图片说明文字不算看图。每篇只精简转述关键方法；后文我方推论另列，不冒充作者验证过我们的试作。

| # | 官方正文／作者／日期 | 实际读到的范围 | 原文方法的精简提取及限制 |
|---|---|---|---|
| 1 | [Chunkification: Creating A Design Language For Sprite Fright](https://studio.blender.org/blog/chunkification-creating-a-design-language-for-sprite-fright/)；Christian Bunyan采访美术指导Andy Goralczyk；2021-02-01 | 从剧情与视觉目标、既往作品参照，经Chunkification定义、人物与物件关系，到Jay收音机删减细节、把角色放在道具旁检查适配；正文末尾 | 把缩小模型的逻辑变成统一取舍：某些特征加粗，另一些删除，人物大手大脚与物件共同调整。收音机从80年代实物参照删去杂乱按钮／贴纸，再检验整体形状和细节节奏。不是“随便把所有东西做胖”；未下载其演变文件。 |
| 2 | [Sprite Fright: Illusion of Simplicity](https://studio.blender.org/blog/sprite-fright-the-illusion-of-simplicity/)；角色艺术家Julien Kaspar；2022-01-13 | Our Inspirations、Balancing Simple & Complex?、Aim for Appeal Instead；到头形六点、嘴／牙／假皱纹及结论；评论不作为制作事实 | 大形与选择性细节统一造型、材质和动画；限制布／发模拟也是制作取舍。作者明确记录早期细节过多后重做，简单头形也需侧面／眼部修形，部分嘴形只为特定机位成立。未把球头当“简化完成”，也未运行角色rig。 |
| 3 | [One Thing I’ve Learned From Sprite Fright: Animation Edition](https://studio.blender.org/blog/one-thing-ive-learned-from-sprite-fright-animation-edition/)；官方采访动画师Pablo Fournier，页面未显示独立署名；2021-04-26 | 开头经历、Motion Blur Without The Motion Blur及其后说明，到相关阅读／订阅区前 | 通过Grease Pencil的快速色形过渡制作smear，服务卡通运动而非直接依靠渲染运动模糊。正文特别指出它应在快速运动中被感到，而非被当作停住的普通姿态阅读。内嵌动态示例未看，不能据文字判定成片某帧的效果或时长。 |
| 4 | [Sprite Fright Workflow: Lighting & Set Dressing](https://studio.blender.org/blog/sprite-fright-workflow-lighting-set-dressing/)；Christian Bunyan采访Beau Gerbrands；2021-08-17 | Beau’s Job六步、Lessons、Faster Lighting五条至正文末 | 镜头初光排进序列，讨论叙事清晰度，再改灯、布景、材质与必要动画，最终EXR合成。接触表查跨镜头明度／角度／道具；渲染版本保留便于对比。遮光物用来降次要物吸引力，并明确避免与物件相交。未使用其插件或实际复刻灯光。 |
| 5 | [Exploring the production files](https://studio.blender.org/blog/exploring-production-files/)；美术指导Andy Goralczyk；2021-11-24 | File structure、Animation files、Effects files、Lighting files及A couple of things to keep in mind全部可得正文 | 单镜头包含依赖，lib放资产、caches放缓存；动画输出供特效／灯光引用，任务文件分开。部分GP效果渲染前转mesh；若分View Layer，合成在灯光文件。旧项目还有脚本、覆盖与旧节点依赖，文章当年的“最新版兼容”不代表2026年5.2已验证。未开包、未启自动脚本。 |
| 6 | [Sprite Fright Edit Bundle](https://studio.blender.org/blog/sprite-fright-edit-bundle/)；Pipeline TD Paul Golter；2021-11-25 | 全文，包括包大小、135版本、目录结构、Story Recap入口 | 作者说明49GB编辑包含135版剪辑、部分弃案，编辑blend、合成预览、OTIO与源媒体分目录。证明可检查的版本材料有组织结构，**不证明我们已看135版或知道哪个弃案为何删掉**；未下载49GB，未观看Recap。 |

补充实读但不计入上表“六篇主读”：[Andy灯光与渲染教程](https://studio.blender.org/blog/Sprite-Fright-Master-Class-Lighting-Rendering/)的可得选段（协作开头、步骤06/07/13–15/18–19/22–24、Pro Tips，**未取得全部中间步骤**）；[Simon材质访谈](https://studio.blender.org/blog/one-thing-ive-learned-from-sprite-fright-shading-edition/)的程序化调整／脚本／Geo Nodes正文。前者给出了以角色接触关键图检验造型和灯光的例子，后者强调可调与复用仍需针对动画角色解决特定问题。二者都不是本轮已完成的教程复作。

## 3. demo及生产文件：已经核到哪一步

[Blender官方demo页](https://www.blender.org/download/demo-files/) 的检索正文把“Blender 3.0 – Sprite Fright”标为Blender Studio、115MB、CC-BY。本轮普通HTTP实际读到 [官方demo目录](https://download.blender.org/demo/) 列有 [sprite_fright_030_0020_A.zip](https://download.blender.org/demo/sprite_fright_030_0020_A.zip)，目录大小为**254,374,945字节**，时间2021-12-14。两处体积并不一致，不能声称已核实demo页115MB条目就一定是这一个254MB包，也不把通用CC-BY标记充当包内每依赖许可核对。

本轮**没有下载、解压或打开此zip**；没有读取其实际对象名、rig、贴图、缓存及许可证文件。所以它是“存在可进一步取用的官方单镜头包”的证据，实际依赖结构目前来自第5篇作者说明，不能写成我们已检查该包内部。若下一步选择它，应先核所需Blender版本和包内说明，隔离审查脚本依赖，再决定是否需要运行；本轮不擅自开自动脚本执行。

Style Guide的介绍页显示有风格约束和下载入口，但没有实际取得完整文档；**不计为全文研读**。Story Development目录多数资产显示Subscribe to view，停在目录，不通过页面列名猜测受限地址。已有公开成片不意味着全部制作资产也都无需订阅。

## 4. 与《Pas de deux》不同的实质比较框架

以下为本研究者根据已读过程文和当前任务提出的比较，**不是对尚未观看《Sprite Fright》成片的验收结论**。

**形体的可控偏离。**《Pas de deux》已看样本中的身体复制是在同一身体的不同时间间建立可见形状；《Sprite Fright》正文讨论的则包括按机位修形、快速smear、道具—人物统一尺度等不同层级。可以有意违背写实，但须说明改变的对象、时段、镜头及识别参照。我们的V2手穿实体板没有表现出这样一套已验证规则，不能在修复前用“风格化”概括掉。

**整体风格必须落到使用关系。**道具简化并非只给一个好看的独立模型。对《最后一张》，110×40厘米纸、外包114×44厘米、两人的手和170厘米身高基准，必须在共同搬运时仍成立。造型可夸张，关键抓边厚度、可握位置和双方支撑空间却不能因简化被删掉。本文没有在角色旁摆过官方道具，此处是我方最小检验建议。

**灯光是跨部门回看的一部分。**当前最缺的是接触、包装状态链和离场因果。仅调漂亮颜色不会使消失的纸产生收纳动作，也不会让板自动有承重。接触表适合发现跨镜头不一致；它也会漏掉smear、释放和短动作。需要在全片概览之外，为手—板、带—包、箱—门建立密帧窗口，随后正常速度检查。

**协作结构不是软件清单。**三维场景的真实好处是角色、包、带、私箱可保有身份并可修改；代价是动画、特效、灯光和剪辑的输出对应必须明确。作者分任务文件的办法可作参考，单人60秒预演不必复制复杂工作室管线。最低限度先保留一份共同资产、一份冻结的机位／节拍表和每次输出对应版本，避免用不同位置／朝向的重画对象假装同一包的连续运动。

**版本数量不是研究深度。**135版编辑确有材料入口，但我们未取得，不能根据数字讲述具体弃案。当前V1/V2已改过多变量，后续应针对已记录失败留下前后同机位、同范围对照，而非继续增加一批“看起来进步”的不同画面。美术研究可以与修复交错，不以学完此片全部资产为《最后一张》创作前提。

## 5. 交给主控的实际观看问题

1. 先本地解码核首末、帧数、显示比例及声音存在；与服务器probe分列，别把15116帧误按630×24硬补到15120帧。
2. 做全段取样，再从真实看见的多人／道具互动中选关键窗口。不要预先指定“某分某秒一定发生托举或包装”；本报告没有该片实看时码。
3. 分别观察：轮廓简化是否仍让手—物接触可辨；快速smear与正常姿态怎样交替；道具从取得、使用到结果是否保持身份；角色位置与机位转换如何维持空间；光色变化是否让关键动作更易读。过程文是可检验解释，不是预填答案。
4. 如只取样静帧，仍不能判断全部运动节奏、眼动引导效果或音画关系。与《最后一张》比较时，只把已经实际看到的同类问题纳入，保留反例和不适用处；不要求我方照用恐怖喜剧、美式卡通或大制作的表面风格。

已完成：一部官方完整公开文件、下载尺寸与哈希、服务器规格、两片稳定官方入口、六篇制作正文的实际文本研读及可转用／不可转用分析。未完成：本子agent对新片的图像／连续视听、工程下载运行、完整Style Guide及135版剪辑研究、我方修订的验收。原片与原始API只本地保存，报告可由主控按资料库既有规则归档。
