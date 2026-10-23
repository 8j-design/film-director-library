# GitHub与开放制作：数字美术的工具、文档及工程研究

研究日期：2026-10-23。新范围允许超出原十题；本稿是研究子任务，主库由主 agent 统一整合。

本轮实际读取 16 个 GitHub 项目的官方 README 正文（含两项官方镜像），另选读 OpenToonz 生产流程、Malt 渲染管线、MaterialX Viewer 的实质文档。这里的“研究”指文本与少量示例代码阅读，没有安装、运行、渲染、下载大型工程、逐个审核源码或观看示例视频/GIF。因此不写“已联动可用”或“艺术效果已验证”。以下来源分支为访问时状态，不把默认分支当稳定发布版本。

## 查重范围

已用精确 repo 名称和主要项目词检索当前 film-director-library 本地工作版及迁移档案的 GitHub库目录（Markdown/CSV/JSON），没有命中。这个结果只覆盖上述本地范围，未遍历旧 my-ai-library 最新远端全部卡片。16 项均标为“本地范围未命中；旧库远端需主写核对”，不宣称全是首次收藏。

## 16 项核验记录

每项都保留问题、可读材料与使用边界。许可栏说明本轮核到哪一层；软件许可不自动覆盖所有第三方资产、截图、品牌或外链案例。并未形成针对具体发行行为的法律意见。

| owner/repo 与主要正文 | 实际阅读范围 | 能解决什么问题／可学材料 | 许可核到的范围／依赖与局限 |
| --- | --- | --- | --- |
| [opentoonz/opentoonz](https://github.com/opentoonz/opentoonz)，[README master](https://raw.githubusercontent.com/opentoonz/opentoonz/master/README.md) | README 全文0–67行；另读下述 production_workflow 全文 | 2D绘制、场景组织的应用源码；README 是软件入口，流程文档才提供分镜、资产、布局、动画接口 | README 明确主体 Modified BSD，并单列 thirdparty 与 MyPaint brushes 例外；未逐文件核。平台/依赖需按目标发行版确认，不把 Toonz 历史等同所有旧功能现可用 |
| [synfig/synfig](https://github.com/synfig/synfig)，[README master](https://raw.githubusercontent.com/synfig/synfig/master/README.md) | 全文0–54行 | 以向量/位图和补间降低逐帧劳动的2D路线；本轮读到功能定位及安装/构建入口，未读动画教程或具体工程 | README 声明 GPLv3；未全读 LICENSE。Windows/Linux/macOS；实际插值、变形和线条表现待作品级测试，不把“film-quality”宣传当结论 |
| [NatronGitHub/Natron](https://github.com/NatronGitHub/Natron)，[README RB-2.6](https://raw.githubusercontent.com/NatronGitHub/Natron/RB-2.6/README.md) | 全文0–126行，重点 Features、Requirements、Installing | 节点合成源码与文档入口；32位浮点线性、OCIO、多通道EXR、遮罩/跟踪使合成不止滤镜拼接 | README GPLv2；插件另核。OpenGL、OIIO/FFmpeg/OpenFX 等依赖。README 的开发/稳定分支说明仍含旧号，不据其断言最新稳定版本；性能描述未本机验证 |
| [bnpr/Malt](https://github.com/bnpr/Malt)，[README Development](https://raw.githubusercontent.com/bnpr/Malt/Development/README.md) | 全文0–46行；另读 Malt/readme.md 全文0–103行含最小管线示例 | NPR可定制渲染框架，含Blender宿主、GLSL节点及Python渲染管线；可学“渲染规则是设计的一部分” | README MIT。Windows/Linux、OpenGL4.5、匹配Blender版本，建议独显；不推荐Windows任务改用Mac路径。面向技术美术，实时不等于任何画面都快 |
| [AcademySoftwareFoundation/MaterialX](https://github.com/AcademySoftwareFoundation/MaterialX)，[README main](https://raw.githubusercontent.com/AcademySoftwareFoundation/MaterialX/main/README.md) | 全文0–71行；Viewer.md全文0–96行 | 材质/Look描述交换；例材质与Open Chess Set是可追踪参考资产入口，不只是API。未打开资产、截图或逐节点图 | README Apache2.0徽标，未逐资产核。C++17/CMake，Python绑定及Viewer可选；不同宿主/着色模型不保证结果逐像素一致 |
| [AcademySoftwareFoundation/OpenColorIO](https://github.com/AcademySoftwareFoundation/OpenColorIO)，[README main](https://raw.githubusercontent.com/AcademySoftwareFoundation/OpenColorIO/main/README.md) | 全文0–124行 | 跨应用色彩管理、显示变换与配置的基础；这是保持判断条件的工具，不替美术决定色调 | README软件BSD3-Clause，文档头CC-BY4.0，并明确影片图像版权；未审第三方全部许可。需匹配应用、配置与显示环境；README历史版本语句不当最新发行号 |
| [PixarAnimationStudios/OpenUSD](https://github.com/PixarAnimationStudios/OpenUSD)，[README release](https://raw.githubusercontent.com/PixarAnimationStudios/OpenUSD/release/README.md) | 全文0–235行；LICENSE.txt开头及授权/再分发段选读0–120行 | 时间采样场景描述与交换；库/示例入口，不是现成电影资产包，未读全部composition文档 | 本次LICENSE为 Tomorrow Open Source Technology License1.0，开头解释与Apache2.0第6节区别，不能沿用旧称“只有Apache”。C++/CMake/TBB及可选Python/查看器依赖；宿主支持需另测 |
| [AcademySoftwareFoundation/OpenTimelineIO](https://github.com/AcademySoftwareFoundation/OpenTimelineIO)，[README main](https://raw.githubusercontent.com/AcademySoftwareFoundation/OpenTimelineIO/main/README.md) | 全文0–183行，含C++/Python示例；LICENSE.txt标题与前部条款选读 | 剪辑顺序、时长和媒体引用交换；它不是媒体容器。可学镜头版、剪辑版与素材引用分离 | LICENSE标题Apache2.0，未审全部适配器。C++核心/Python；0.16之后适配器分包，本轮不测任何NLE导入，不将读取AAF示例当全格式无损 |
| [processing/p5.js](https://github.com/processing/p5.js)，[README main](https://raw.githubusercontent.com/processing/p5.js/main/README.md) | 全文0–99行及极小setup/draw示例；license.txt标题/前部选读 | 浏览器中的生成、互动与声画草图；可学规则、循环、输入如何构成表达。本轮没有浏览/运行外链作品 | license.txt为LGPL2.1；未审社区外部库。需浏览器/JS能力；输出固定影片时还需确定时间、输入和导出，不把交互草图当完成电影 |
| [nannou-org/nannou](https://github.com/nannou-org/nannou)，[README master](https://raw.githubusercontent.com/nannou-org/nannou/master/README.md) | 全文0–83行；示例目录说明与库表，不是目录内源码全读 | Rust创意编程，含生成设计、Nature of Code移植及音频/ISF/OSC等入口；可扩展非人物、非传统叙事方向 | README链接称Apache/MIT双许可路线；两次直接许可文件请求404/Cache miss，未核文件全文。Rust/Cargo及GPU/平台环境；当前master称基于Bevy，不能把旧教程架构默认套上 |
| [ossia/score](https://github.com/ossia/score)，[README master](https://raw.githubusercontent.com/ossia/score/master/README.md) | 全文0–83行；LICENSE.txt前14行第三方列表及GPLv3标题 | 多软件/设备的互动声画“谱”，OSC/MIDI/DMX/视频等；与固定时间线影片不同，可学事件和跨媒介关系 | GPLv3标题、第三方例外列表已核，未全核子模块。桌面等多目标；协议/设备与外部软件仍需匹配，不能说仅装它就联动所有软件 |
| [vuo/vuo](https://github.com/vuo/vuo)，[README main](https://raw.githubusercontent.com/vuo/vuo/main/README.md) | 全文0–134行；LICENSE.md五行全文 | 节点编程系统源码/构建指南；本轮尚未读具体composition教程，艺术材料深度弱于Malt/MaterialX | LICENSE区分大多数Community组件LGPL2+与非Pro节点/示例MIT，要求逐文件确认。README主要macOS构建，Xcode/Homebrew/Conan等；本机Windows不作为优先安装候选 |
| [godotengine/godot](https://github.com/godotengine/godot)，[README master](https://raw.githubusercontent.com/godotengine/godot/master/README.md) | 全文0–67行 | 2D/3D实时世界、互动叙事和预演的引擎入口；本轮未读动画混合、Movie Maker或完整项目，不能称电影流程已研究 | README MIT及官方文档/例工程链接；平台与目标导出约束待查。游戏引擎不自动提供完整离线摄影/合成工作流 |
| [icosa-foundation/open-brush](https://github.com/icosa-foundation/open-brush)，[README main](https://raw.githubusercontent.com/icosa-foundation/open-brush/main/README.md) | 选读0–122行，含定位、发布差异、VR/Unity构建、开源替代；LICENSE标题及主体条款 | 空间绘画/VR路径，扩展平面风格板以外的身体、笔触与场景关系；未操作VR或看示例艺术 | LICENSE Apache2.0；README另列Tilt Brush商标、部分原组件替换。Unity及设备/运行时版本；实验画笔保存与正式版可显示不同，不写免费软件=零硬件成本 |
| [blender/blender](https://github.com/blender/blender)，[README main](https://raw.githubusercontent.com/blender/blender/main/README.md) | 全文0–36行 | 3D全流程应用源码入口；代码仓库本身不能代替完整电影的设计/生产档案。实际开发页指向projects.blender.org | README整体GPLv3、个别兼容许可；未审所有文件。平台/硬件未在这个短README细读；电影工程另见下方Gold辨误 |
| [KDE/krita](https://github.com/KDE/krita)，[README master](https://raw.githubusercontent.com/KDE/krita/master/README.md) | 全文0–111行 | 数字绘画、概念/接景/纹理的源码入口；艺术手册另链，未据README声称动画练习已做 | README整体GPLv3与个别兼容许可。明确GitHub只是镜像，主仓invent.kde.org/graphics/krita；依赖/笔刷资产须分别核，未安装 |

## 四个值得继续深读的方法问题

以下是研究推论及后续验证设计，不是完成的技术/艺术测试。引用的具体功能来自已读官方文档，自己的判断不能反向冒充项目作者结论。

### 一、OpenToonz：设计是否从一开始就包含可动性和生产分解？

附加正文：[production_workflow.rst](https://raw.githubusercontent.com/opentoonz/opentoonz_docs/master/source/production_workflow.rst)，全文0–164行；代码库为opentoonz/opentoonz_docs。它把分镜连接到所需角色姿态、道具、背景，动态分镜包含计时/镜头/参考音轨；布局继续细化而非重新开始；也举出把转轴藏入造型特征的例子。

研究判断：前期人物形象不能只有正面漂亮立绘，还应问其动作怎样暴露/隐藏连接，近景与转面怎样成立。不过文档的paperless流程特别接近部件动画，不能将“藏转轴”强推到逐帧、变形动画或实验电影。扫描章节仍需与版本功能另核；扫描专页明确原生扫描不支持、保留历史文档，此处不把总流程旧示意当现可执行承诺。

### 二、Malt：风格是绘画滤镜，还是一套可控制的成像规则？

附加正文：[Malt/readme.md](https://raw.githubusercontent.com/bnpr/Malt/Development/Malt/readme.md)，全文0–103行，含最小Python/GLSL示例。宿主负责场景数据，Pipeline决定参数、材料编译、渲染目标和结果；文档明确比性能更重质量、灵活性和简单性。

研究判断：若以后要讨论轮廓遮挡、明暗组织、局部笔触和不同层次的视觉关系，可以先定义哪些关系必须受控，再判断是否需要定制渲染。它并不证明“越可编程越好”；可调项过多会使整体表达失去约束，维护渲染器也可能吞掉独立制作的创作时间。优先看NPR实例与对应连续镜头，再决定是否接入，不能为工具反过来改题材。

### 三、MaterialX／OCIO：把材质选择和观看条件分开记录

附加正文：[MaterialX Viewer](https://raw.githubusercontent.com/AcademySoftwareFoundation/MaterialX/main/documents/DeveloperGuide/Viewer.md)，全文0–96行。它分开加载几何、材质和环境，允许参数编辑与wedge比较；不是一张最终场景图的万能替代。

研究判断：以后做材质比较应先固定一部分条件，再改变粗糙度、纹理尺度等目标变量，并回到作品照明复核。OCIO负责跨应用观看条件的一致性，MaterialX负责材质描述交换，两者不能互相替代。外观变了既可能是美术修改，也可能只是视图变换/光照不同；没有区分就难以复盘。标准材质球不含人物、构图和运动，因此测试通过不等于镜头表达成立。

### 四、OTIO／USD／ossia：不同“联动”实际上保存不同关系

三者已读README分别涉及剪辑时序、场景描述、互动跨媒介事件。不能因为都能交换数据，就把它们写成一条已经打通的管线。

研究判断：先确定创作要固定的是“镜头怎样连接”“世界/资产怎样组合”还是“什么事件引发什么声画”。再定义应保存哪些版本、时间基准与外部引用。线性短片可能只需轻量时间线和资产命名；互动或装置作品则需要考虑输入条件、重复运行和不可预测时长。复杂标准不是成熟的代名词，反之只保存一段最终视频又可能丢失重构能力。

## 开放电影工程：Gold 的重要边界与未完成部分

本轮没有找到并取得“GitHub上官方Project Gold完整电影工程”。不拿搜索命中的第三方学习库、awesome清单或电影追踪应用充数。

官方检索可见材料：

- [Project Gold Update](https://studio.blender.org/blog/project-gold-update/)，Francesco Siddi，2024-04-08：检索正文明确原电影制作停止，改做精选镜头与分解的showcase。直接打开返回402；本项仅记官方索引正文，不记全文研读。
- [Project Gold Premiere](https://studio.blender.org/blog/project-gold-premiere/)，Francesco Siddi，2024-11-07：官方检索正文称technical showcase，并说明订阅可取得工作坊和生产文件。直接打开402。
- [260_0050 Shot Files](https://studio.blender.org/projects/gold/3d823d3a8c9db8/?asset=7529)，Andy Goralczyk，2024-11-11：官方索引可见anim/fx/caches/lighting/comp结构、1.2GB、Blender4.2、lighting至少64GB内存/swap与CC-BY4.0说明；页面有登录/订阅提示，直接打开402。未下载、未验证、未执行其中启动脚本要求。

因此Gold目前是“官方过程与分工、访问/资源条件的候选证据”，不是已取得的完整开放电影，不归入16项GitHub正文。本批未购买订阅；仍要另找能合法实际读取、体量适合的完整开放片工程及从设计到成片的版本对照，公开材料也可继续研究。

## 尚未被本批覆盖的方向

这16项多数是创作工具或数据基础，不等于16个完整艺术学习案例。还缺：实际独立短片工程及弃案、程序生成的作者作品与长期迭代、笔触时间一致性、传统手工/定格的数字混合、实时视觉与空间展演、可访问性/不同显示载体、制作经济与可持续维护。原十题可用来交叉索引，但不封顶；作品问题比凑仓库数量更重要。

下一步应从三类材料各取一件深入：一套可取得的完整片工程、一份有作者意图与修改史的实验作品、一段可复核的NPR连续镜头。只在具体表达问题要求时才试用对应工具。现在没有必须让用户补账号或登录的阻塞，可以继续读公开过程材料。
