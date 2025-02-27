# 📚 Elsevier-Review-Tracker  
**爱思维尔期刊审编进度跟踪工具**  

---

## ✨ 功能介绍  
本项目用于获取 **Elsevier 期刊** ，在投稿论文进入 **"Under Review"** 状态后的 **审稿进度**，帮助研究人员更方便地跟踪投稿状态，包括：  

### 📝 论文基本信息  
- 论文标题  
- 投稿编号  
- 期刊名称  
- 第一作者  
- 通认作者  
- 投稿时间  
- 最近更新时间  
- 当前修改版本  

### 📊 审编进度信息  
- **审编状态统计**  
- **详细审编过程**（包含时间、事件、版本、ID）  

### 📰 支持多期刊  
- 适用于 **Elsevier** 方出的几乎所有期刊  

---

## 🔧 安装与使用  

### 1️⃣ 环境依赖  
请确保已安装 **Python** 环境，并安装以下第三方库：  

```bash  
pip install requests json uuid time collections  
```

**注意：** 因输出信息包含中文字符，请确保文件编码、Python 代码、终端/控制台编码、数据处理方式以及显示字体均支持中文，以正确显示输出信息

### 2️⃣ 使用方法  
首先在 `Elsevier-Review-Tracker.py` 文件中补充L190-L194中的待查询的论文编号、通讯作者姓、名：

```bash  
manuscript_id = get_manuscript_id(
            manuscript_number="",# 引号内填论文编号，如JII-D-xx-xxxxx
            last_name="",# 引号内填通讯作者姓
            first_name=""# 引号内填通讯作者名
        )  
```

接着运行 `Elsevier-Review-Tracker.py` 文件即可：  

```bash  
python Elsevier-Review-Tracker.py  
```

---

## ⚠️ 使用须知  
- 本工具**仅用于个人研究用途**，不涉及任何 **黑客行为**，所有数据均来自用户授权访问的 **Elsevier Manuscript System**。  
- 请**确保符合期刊的使用条款**，避免过于频繁查询，以防御平台小骄。  

---

## 📌 未来改进方向  
- **🛠️ 暂无计划**，如有建议欢迎提交 Issue 或 Pull Request！  

---

## 🛠 贡献与支持  
欢迎 **Star ⭐** 和 **Fork 🍴** 本项目！    
