import os
import sys
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#64748B"))
        
        # Header (pages > 1)
        if self._pageNumber > 1:
            self.drawString(36, 810, "TRENVO — Music Trend Predictor & Analytics System")
            self.setFont("Helvetica", 8)
            self.drawRightString(559, 810, "Technology Stack Documentation (Hinglish)")
            self.setStrokeColor(colors.HexColor("#E2E8F0"))
            self.setLineWidth(0.6)
            self.line(36, 804, 559, 804)
            
        # Footer
        self.setStrokeColor(colors.HexColor("#E2E8F0"))
        self.setLineWidth(0.6)
        self.line(36, 38, 559, 38)
        
        self.setFont("Helvetica", 8)
        self.drawString(36, 26, "TRENVO Tech Stack Guide | Machine Learning, Live APIs & Web GUI Architecture")
        self.setFont("Helvetica-Bold", 8)
        self.drawRightString(559, 26, f"Page {self._pageNumber} of {page_count}")
        self.restoreState()


def generate_pdf(output_filename):
    doc = SimpleDocTemplate(
        output_filename,
        pagesize=A4,
        leftMargin=36,
        rightMargin=36,
        topMargin=42,
        bottomMargin=46
    )

    # Custom colors
    c_primary = colors.HexColor("#1DB954")     # Spotify Green
    c_dark = colors.HexColor("#0F172A")        # Slate 900
    c_text = colors.HexColor("#1E293B")        # Slate 800
    c_sub = colors.HexColor("#334155")

    title_style = ParagraphStyle(
        'DocTitle',
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=colors.white,
        spaceAfter=3
    )

    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        fontName='Helvetica',
        fontSize=9.5,
        leading=13,
        textColor=colors.HexColor("#E2E8F0"),
        spaceAfter=2
    )

    h1_style = ParagraphStyle(
        'SectionH1',
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=c_dark,
        spaceBefore=8,
        spaceAfter=4,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'SectionH2',
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=13.5,
        textColor=colors.HexColor("#0F5132"),
        spaceBefore=6,
        spaceAfter=2,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'BodyHinglish',
        fontName='Helvetica',
        fontSize=8.2,
        leading=11.8,
        textColor=c_text,
        spaceAfter=4
    )

    bullet_style = ParagraphStyle(
        'BulletHinglish',
        fontName='Helvetica',
        fontSize=8.2,
        leading=11.6,
        textColor=c_text,
        leftIndent=10,
        spaceAfter=2.5
    )

    table_header = ParagraphStyle(
        'TableHeader',
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10.5,
        textColor=colors.white,
        alignment=0
    )

    table_cell = ParagraphStyle(
        'TableCell',
        fontName='Helvetica',
        fontSize=7.2,
        leading=9.5,
        textColor=c_text
    )

    table_cell_bold = ParagraphStyle(
        'TableCellBold',
        fontName='Helvetica-Bold',
        fontSize=7.2,
        leading=9.5,
        textColor=colors.HexColor("#0F172A")
    )

    story = []

    # ═════════════════════════════════════════════════════════════════
    # PAGE 1: TITLE BANNER + OVERVIEW + COMPLETE TECH SUMMARY TABLE
    # ═════════════════════════════════════════════════════════════════
    banner_content = [
        [
            Paragraph("🎵 <b>TRENVO — Music Trend Predictor & Analytics System</b>", title_style),
        ],
        [
            Paragraph("Complete Technology Stack & Architecture Documentation (Hinglish)", subtitle_style)
        ],
        [
            Paragraph("<font color='#86EFAC'><b>Core Stack:</b> Python 3.14 · Streamlit · Scikit-Learn · Pandas · NumPy · Plotly · Requests · REST APIs · HTML5/CSS3 · Cloud</font>", subtitle_style)
        ]
    ]
    banner_table = Table(banner_content, colWidths=[523])
    banner_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#0B132B")),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
        ('RIGHTPADDING', (0,0), (-1,-1), 12),
        ('TOPPADDING', (0,0), (-1,-1), 9),
        ('BOTTOMPADDING', (0,0), (-1,-1), 9),
        ('LINEBELOW', (0,-1), (-1,-1), 3, c_primary),
    ]))
    story.append(banner_table)
    story.append(Spacer(1, 6))

    # 1. Project Overview
    story.append(Paragraph("1. Project Overview & Multi-Layered Architecture", h1_style))
    story.append(Paragraph(
        "<b>TRENVO</b> ek end-to-end <b>Music Trend Analytics aur Predictive AI Platform</b> hai. Is project ka main objective 1,14,000 Spotify tracks aur live streaming charts ko analyze karke music industry ke viral trends detect karna aur naye songs ke audio characteristics ke basis par unka trend potential predict karna hai.<br/>"
        "Project ko <b>3 integrated layers</b> par construct kiya gaya hai: (1) <b>Data Layer:</b> Raw dataset cleaning, feature engineering aur weighted score calculation. (2) <b>ML Layer:</b> Random Forest model se hit probability prediction. (3) <b>Web & API Layer:</b> Multi-page interactive Streamlit dashboard aur real-time Apple Music REST APIs.",
        body_style
    ))
    story.append(Spacer(1, 4))

    # 2. Tech Reference Table
    story.append(Paragraph("2. Quick Technology Reference Matrix", h1_style))

    tech_table_data = [
        [
            Paragraph("Technology", table_header),
            Paragraph("Category", table_header),
            Paragraph("File / Module", table_header),
            Paragraph("Role & Purpose (Kisme kya use hui)", table_header)
        ],
        [
            Paragraph("<b>Python 3.14</b>", table_cell_bold),
            Paragraph("Core Language", table_cell),
            Paragraph("All scripts (`src/`, `gui/`)", table_cell),
            Paragraph("Pura backend logic, data transformation, ML model training, API communication aur GUI script.", table_cell)
        ],
        [
            Paragraph("<b>Streamlit</b>", table_cell_bold),
            Paragraph("Web UI Framework", table_cell),
            Paragraph("`gui/app.py`", table_cell),
            Paragraph("Multi-page interactive web GUI (7 Pages: Dashboard, Rankings, Artist Search, Head-to-Head, AI Predictor).", table_cell)
        ],
        [
            Paragraph("<b>Scikit-Learn</b>", table_cell_bold),
            Paragraph("Machine Learning", table_cell),
            Paragraph("`src/prediction.py`<br/>`gui/app.py`", table_cell),
            Paragraph("`RandomForestClassifier` train karke audio features se trending probability (0-100%) predict karna.", table_cell)
        ],
        [
            Paragraph("<b>Pandas</b>", table_cell_bold),
            Paragraph("Data Engineering", table_cell),
            Paragraph("`data_cleaning.py`<br/>`feature_engineering.py`<br/>`app.py`", table_cell),
            Paragraph("114,000+ tracks ka dataset load, clean, deduplicate, filter, group aggregate aur sort karna.", table_cell)
        ],
        [
            Paragraph("<b>NumPy</b>", table_cell_bold),
            Paragraph("Numerical Computing", table_cell),
            Paragraph("`feature_engineering.py`<br/>`gui/app.py`", table_cell),
            Paragraph("Mathematical formulas, probability scaling, score clipping (`np.clip`), fast array computations.", table_cell)
        ],
        [
            Paragraph("<b>Plotly</b>", table_cell_bold),
            Paragraph("Interactive Data Viz", table_cell),
            Paragraph("`gui/app.py`", table_cell),
            Paragraph("Modern dark charts: Horizontal bars, Gauge score meter, Head-to-head comparison bars, timelines.", table_cell)
        ],
        [
            Paragraph("<b>Joblib</b>", table_cell_bold),
            Paragraph("Model Serialization", table_cell),
            Paragraph("`model/trend_model.pkl`<br/>`src/prediction.py`", table_cell),
            Paragraph("Trained Random Forest model aur aligned feature columns ko disk par save aur app me fast load karna.", table_cell)
        ],
        [
            Paragraph("<b>Requests (APIs)</b>", table_cell_bold),
            Paragraph("Networking / REST", table_cell),
            Paragraph("`gui/app.py`", table_cell),
            Paragraph("Apple Music RSS Feed (Top 100 live), iTunes Search API, aur MusicBrainz se live metadata fetch karna.", table_cell)
        ],
        [
            Paragraph("<b>HTML5 & CSS3</b>", table_cell_bold),
            Paragraph("UI & Glassmorphism", table_cell),
            Paragraph("`GLOBAL_CSS` in `app.py`", table_cell),
            Paragraph("Spotify-style dark aesthetic, animated equalizer bars, live ticker tape, glass cards aur custom scrollbars.", table_cell)
        ],
        [
            Paragraph("<b>Jupyter Notebook</b>", table_cell_bold),
            Paragraph("EDA & Research", table_cell),
            Paragraph("`notebooks/analysis.ipynb`", table_cell),
            Paragraph("Raw data exploration, preliminary trends, top artists aur statistical distributions inspect karna.", table_cell)
        ],
        [
            Paragraph("<b>Matplotlib / Seaborn</b>", table_cell_bold),
            Paragraph("Static Plotting", table_cell),
            Paragraph("`notebooks/analysis.ipynb`", table_cell),
            Paragraph("Exploratory phase me correlation heatmaps, feature distribution histograms aur scatter plots draw karna.", table_cell)
        ],
        [
            Paragraph("<b>Git & GitHub</b>", table_cell_bold),
            Paragraph("Version Control", table_cell),
            Paragraph("`.git/` repository", table_cell),
            Paragraph("Source code tracking, commits, branch sync (`main`), and continuous deployment sync with cloud.", table_cell)
        ],
        [
            Paragraph("<b>Streamlit Cloud</b>", table_cell_bold),
            Paragraph("Cloud Deployment", table_cell),
            Paragraph("Production URL", table_cell),
            Paragraph("App ko 24x7 online URL par host karna taaki laptop band hone par bhi phone aur desktop par chale.", table_cell)
        ]
    ]

    t = Table(tech_table_data, colWidths=[80, 80, 110, 253])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0F172A")),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 2.2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.2),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")]),
    ]))
    story.append(t)

    # ═════════════════════════════════════════════════════════════════
    # PAGE 2: DETAILED TECH BREAKDOWN (PART 1: Python, Streamlit, ML, Pandas)
    # ═════════════════════════════════════════════════════════════════
    story.append(PageBreak())
    story.append(Paragraph("3. Detailed Technology Breakdown (Kisme Kya Use Hui Hai)", h1_style))
    story.append(Paragraph(
        "Is section me har ek technology ko practical flow me explain kiya gaya hai ki wo project ke kaunse module me lagi hai aur uska real-world purpose kya hai:",
        body_style
    ))
    story.append(Spacer(1, 4))

    # Tech 1: Python
    story.append(Paragraph("🐍 1. Python (Core Programming Language)", h2_style))
    story.append(Paragraph(
        "<b>Kisme use hui:</b> Pure project ka foundation Python hi hai — data ingestion, cleaning, ML model training, API communication, aur Streamlit web GUI sabhi Python scripts me execute hote hain.<br/>"
        "• <b>Kyun use ki gayi:</b> Python data science aur Machine Learning ka standard global ecosystem hai. Isme robust data manipulation (Pandas), ML algorithms (Scikit-Learn), numerical computing (NumPy), aur rapid web application frameworks (Streamlit) ka seamless integration milta hai.<br/>"
        "• <b>Primary Source Files:</b> `src/data_cleaning.py`, `src/feature_engineering.py`, `src/prediction.py`, `gui/app.py`.",
        bullet_style
    ))
    story.append(Spacer(1, 4))

    # Tech 2: Streamlit
    story.append(Paragraph("⚡ 2. Streamlit (Frontend Web Framework & Interactive Dashboard)", h2_style))
    story.append(Paragraph(
        "<b>Kisme use hui:</b> `gui/app.py` (Project ka main visual presentation platform).<br/>"
        "• <b>Kya kaam karti hai:</b> Yeh bina complex HTML/React/Node boilerplate ke seedhe Python scripts ko fast, responsive, web dashboard me badal deta hai.<br/>"
        "• <b>Project ke 7 Core Pages jo Streamlit se bane hain:</b><br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;1. <b>Dashboard:</b> Real-time #1 trending song display, 4 summary KPI cards (Tracked songs, Trending songs, Top Artist, Top Genre), live moving ticker tape, aur genre analysis.<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;2. <b>Top 10 Rankings:</b> Leaderboard jisme user Trend Score, Popularity ya Growth % ke hisaab se dynamically sort kar sakta hai.<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;3. <b>Artist Search:</b> Artist ka naam enter karte hi live track counts, average trend score, origin country, aur top tracks cards display karta hai.<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;4. <b>Artist vs Artist (Head-to-Head):</b> Do artists ke beech direct comparison — simplified horizontal side-by-side bars aur table jo winner decide karta hai.<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;5. <b>Genre Intelligence:</b> Pop, Hip-Hop, Rock, Dance, R&B, K-Pop wagera ke category charts alag-alag tabs me render karta hai.<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;6. <b>Weekly Trends:</b> 8 hafton ka continuous momentum timeline curve draw karta hai jo song ki trajectory visualize karta hai.<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;7. <b>AI Predictor:</b> Interactive audio feature sliders provide karta hai jisse model real-time trend potential predict karta hai.<br/>"
        "• <b>Built-in Features Used:</b> `st.cache_data` (API calls ko 30-60 min cache karke rate-limit se bachana), `st.columns`, `st.tabs`, `st.sidebar`, `st.form`, `st.slider`.",
        bullet_style
    ))
    story.append(Spacer(1, 4))

    # Tech 3: Scikit-Learn & Joblib
    story.append(Paragraph("🤖 3. Scikit-Learn & Joblib (Machine Learning Engine)", h2_style))
    story.append(Paragraph(
        "<b>Kisme use hui:</b> `src/prediction.py` (Offline Training) aur `gui/app.py` (Real-time Online Inference).<br/>"
        "• <b>Algorithm Architecture:</b> `RandomForestClassifier` (100 Decision Trees, parallel processing via `n_jobs=-1`).<br/>"
        "• <b>Model Training Workflow:</b><br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;• <b>Dataset Partition:</b> `train_test_split` se 80% data training aur 20% validation ke liye split kiya gaya.<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;• <b>Target Definition:</b> Continuous `trend_score` se binary target `trending` banaya gaya (`trend_score >= 75` = Trending).<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;• <b>Feature Encoding & Handling:</b> Categorical text columns ko One-Hot Encoding (`pd.get_dummies`) kiya aur missing values median se fill kiye.<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;• <b>Evaluation Metrics:</b> `accuracy_score` aur `classification_report` se Precision, Recall aur F1-Score analyze kiya gaya.<br/>"
        "• <b>Joblib Persistence:</b> Trained Random Forest model aur one-hot encoded columns ko `model/trend_model.pkl` me serialize kiya gaya, jisse GUI startup time 10x fast ho gaya.<br/>"
        "• <b>Live Scoring Inference:</b> App me user ke input audio features ko aligned columns me transform karke `model.predict_proba()` se exact trending probability nikali jaati hai.",
        bullet_style
    ))
    story.append(Spacer(1, 4))

    # Tech 4: Pandas & NumPy
    story.append(Paragraph("📊 4. Pandas & NumPy (Data Processing & Mathematical Modeling)", h2_style))
    story.append(Paragraph(
        "<b>Kisme use hui:</b> `src/data_cleaning.py`, `src/feature_engineering.py`, `src/weekly_trend_simulation.py`, `gui/app.py`.<br/>"
        "• <b>Data Cleaning Pipeline (`data_cleaning.py`):</b><br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;• Raw Spotify dataset me se 1,14,000 records me se exact duplicate rows aur duplicate `track_id` drop kiye gaye.<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;• 14 core numeric audio columns (danceability, energy, loudness, tempo, acousticness, etc.) ko sanitize aur typecast kiya gaya.<br/>"
        "• <b>Domain Feature Engineering (`feature_engineering.py`):</b><br/>"
 
 
        "&nbsp;&nbsp;&nbsp;&nbsp;• Music industry logic ke hisaab se custom continuous score derive kiya gaya:<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<b>trend_score = (Popularity * 0.6) + (Danceability * 100 * 0.2) + (Energy * 100 * 0.2)</b><br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;• GroupBy aggregations se artist-level aur genre-level average trend benchmarks generate kiye gaye.<br/>"
        "• <b>NumPy Mathematics:</b> Array clipping (`np.clip` between 0.0 and 1.0), dynamic feature distances, safe standard deviations, aur multi-signal weight aggregations.",
        bullet_style
    ))

    # ═════════════════════════════════════════════════════════════════
    # PAGE 3: DETAILED TECH BREAKDOWN (PART 2: Plotly, APIs, CSS, EDA, Git)
    # ═════════════════════════════════════════════════════════════════
    story.append(PageBreak())

    # Tech 5: Plotly
    story.append(Paragraph("📈 5. Plotly Express & Graph Objects (Interactive Visualizations)", h2_style))
    story.append(Paragraph(
        "<b>Kisme use hui:</b> `gui/app.py` me saare rich interactive data charts render karne ke liye.<br/>"
        "• <b>Plotly vs Traditional Matplotlib:</b> Matplotlib static image file banata hai jisme interaction nahi hoti. Plotly vector-based interactive SVG charts deta hai jisme hover tooltips, zoom, toggle legends aur mobile responsive resizing built-in milta hai.<br/>"
        "• <b>Specific Visual Charts in TRENVO:</b><br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;• <b>Dark Horizontal Bar Charts:</b> Top 10 tracks aur hottest genres ki rankings ko vibrant Viridis/Green palettes ke sath plot karta hai.<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;• <b>Interactive Gauge / Dial Indicator:</b> AI Predictor section me gaane ka viral trend score 0 se 100 color-coded threshold zones (Red, Yellow, Green) ke sath display karta hai.<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;• <b>Side-by-Side Comparison Bars:</b> Artist Head-to-Head page par Trend Score, Popularity, Peak Score aur Consistency ko clean horizontal Green vs Purple bars me compare karta hai.<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;• <b>Momentum Area / Scatter Timeline:</b> Weekly Trends page par 8-week trend trajectory curve create karta hai.",
        bullet_style
    ))
    story.append(Spacer(1, 4))

    # Tech 6: Requests & REST APIs
    story.append(Paragraph("🌐 6. Requests Library & Live Music REST APIs", h2_style))
    story.append(Paragraph(
        "<b>Kisme use hui:</b> `gui/app.py` ke real-time network fetching functions me.<br/>"
        "• <b>Kyun zaroori thi:</b> Sirf static CSV data use karne se gaano ke trends purane ho jaate hain. TRENVO live web APIs se fresh global charts sync karta hai.<br/>"
        "• <b>Integrated REST APIs:</b><br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;• <b>Apple Music / iTunes RSS Feed API:</b> Official JSON RSS endpoints se real-time Top 100 songs, chart ranks, album artwork URLs, aur genre-wise feeds fetch kiye jaate hain (No API key needed, zero billing).<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;• <b>iTunes Search API:</b> Jab user kisi artist ka naam enter karta hai, tab specific artist ke top 20 releases, collection name aur release dates query ki jaati hain.<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;• <b>MusicBrainz API:</b> Open community music encyclopedia se artist ka origin country, career start year, band type aur music tags retrieve hote hain.<br/>"
        "• <b>Fault Tolerance & Caching:</b> `@st.cache_data(ttl=1800)` se API responses 30 minutes cache hote hain. Agar API unreachable ho, toh system automatically local dataset par fallback kar leta hai.",
        bullet_style
    ))
    story.append(Spacer(1, 4))

    # Tech 7: HTML5 & CSS3
    story.append(Paragraph("🎨 7. Modern HTML5 & CSS3 (Glassmorphism & Spotify Dark UI)", h2_style))
    story.append(Paragraph(
        "<b>Kisme use hui:</b> `gui/app.py` me `GLOBAL_CSS` block aur HTML card components me.<br/>"
        "• <b>Spotify Dark Design Aesthetics:</b> Background me pitch-black `#050505` ke sath radial gradients (`#1DB954` aur `#7B2FBE`) ka subtle ambient glow set kiya gaya hai.<br/>"
        "• <b>Glassmorphism:</b> Translucent glass background with `backdrop-filter: blur(16px)` aur subtle borders jo sleek, modern web app feel deti hain.<br/>"
        "• <b>Animated Equalizer Bars:</b> Pure CSS `@keyframes` se 4 dynamic audio visualizer bars banayi gayi hain jo top trending track ke sath animated pulse karti hain.<br/>"
        "• <b>Live Stock-Market Ticker:</b> Continuous horizontal scrolling ticker jo live trending gaano ko screen par continuous loop me pass karta hai.",
        bullet_style
    ))
    story.append(Spacer(1, 4))

    # Tech 8: Jupyter, Matplotlib & Seaborn
    story.append(Paragraph("🔬 8. Jupyter Notebook, Matplotlib & Seaborn (Exploratory Data Analysis)", h2_style))
    story.append(Paragraph(
        "<b>Kisme use hui:</b> `notebooks/analysis.ipynb`.<br/>"
        "• <b>Exploratory Phase:</b> Machine learning pipeline build karne se pehle dataset ki distributions, outliers, aur correlation patterns analyze karne ke liye Jupyter environment use hua.<br/>"
        "• <b>Visuals generated:</b> Danceability vs Energy scatter plots, popularity distribution histograms, aur genre frequency distributions inspect kiye gaye.",
        bullet_style
    ))
    story.append(Spacer(1, 4))

    # Tech 9: Git, GitHub & Streamlit Cloud
    story.append(Paragraph("☁️ 9. Git, GitHub & Streamlit Community Cloud (Deployment & Mobile Access)", h2_style))
    story.append(Paragraph(
        "<b>Kisme use hui:</b> Production & Remote Hosting Architecture.<br/>"
        "• <b>Git & GitHub:</b> Pure project ka code GitHub repository (`Tannuverma-77/TRENVO`) par version controlled hai. Har code update `main` branch me push hota hai.<br/>"
        "• <b>Streamlit Community Cloud:</b> Project ko free cloud server par continuous deployment (CD) ke sath deploy kiya gaya hai.<br/>"
        "• <b>Mobile Access Advantage:</b> Local server (`localhost`) sirf us machine par chalta hai jisme project store hai. Cloud hosting se ek permanent secure HTTPS link milta hai, jisse <b>laptop band hone par bhi koi bhi user apne smartphone ya kisi bhi web browser par website seamlessly open kar sakta hai</b>.",
        bullet_style
    ))

    # ═════════════════════════════════════════════════════════════════
    # PAGE 4: FOLDER STRUCTURE MAPPING + SUMMARY CONCLUSION
    # ═════════════════════════════════════════════════════════════════
    story.append(PageBreak())
    story.append(Paragraph("4. Project Folder Structure & Associated Technologies", h1_style))
    story.append(Paragraph("Niche diye gaye chart me project folder structure aur unme mapped technologies ka breakdown hai:", body_style))
    story.append(Spacer(1, 2))

    struct_data = [
        [Paragraph("Folder / File", table_header), Paragraph("Tech Stack Mapped", table_header), Paragraph("Functional Description (Kaam kya hai)", table_header)],
        [
            Paragraph("`data/raw/`", table_cell_bold),
            Paragraph("CSV Data Storage", table_cell),
            Paragraph("Original Spotify tracks dataset (`music_data.csv`) holding 1,14,000 raw records.", table_cell)
        ],
        [
            Paragraph("`data/processed/`", table_cell_bold),
            Paragraph("Pandas / Cleaned CSV", table_cell),
            Paragraph("Cleaned dataset, feature engineered dataset, aur simulated 4-week historical trends.", table_cell)
        ],
        [
            Paragraph("`src/data_cleaning.py`", table_cell_bold),
            Paragraph("Python, Pandas", table_cell),
            Paragraph("Removes duplicate track_ids, sanitizes numeric values, fills missing text attributes.", table_cell)
        ],
        [
            Paragraph("`src/feature_engineering.py`", table_cell_bold),
            Paragraph("Python, Pandas, NumPy", table_cell),
            Paragraph("Calculates continuous `trend_score`, artist averages aur genre averages.", table_cell)
        ],
        [
            Paragraph("`src/prediction.py`", table_cell_bold),
            Paragraph("Scikit-Learn, Joblib", table_cell),
            Paragraph("Trains RandomForestClassifier on trend features and exports serialized model.", table_cell)
        ],
        [
            Paragraph("`src/weekly_trend_simulation.py`", table_cell_bold),
            Paragraph("Python, Random, Pandas", table_cell),
            Paragraph("Simulates 4 weeks of historical fluctuations for longitudinal trend curves.", table_cell)
        ],
        [
            Paragraph("`model/trend_model.pkl`", table_cell_bold),
            Paragraph("Joblib Pickle", table_cell),
            Paragraph("Serialized trained AI model + aligned one-hot feature column headers.", table_cell)
        ],
        [
            Paragraph("`gui/app.py`", table_cell_bold),
            Paragraph("Streamlit, Plotly, Requests, CSS", table_cell),
            Paragraph("Main 7-page interactive dashboard combining ML, live APIs, and custom charts.", table_cell)
        ],
        [
            Paragraph("`notebooks/analysis.ipynb`", table_cell_bold),
            Paragraph("Jupyter, Matplotlib, Seaborn", table_cell),
            Paragraph("Exploratory Data Analysis (EDA) of music tracks and artist profiles.", table_cell)
        ],
        [
            Paragraph("`requirements.txt`", table_cell_bold),
            Paragraph("pip Package Manager", table_cell),
            Paragraph("List of all required dependencies for zero-error installation & cloud deploy.", table_cell)
        ],
        [
            Paragraph("`docs/`", table_cell_bold),
            Paragraph("PDF / Documentation", table_cell),
            Paragraph("Project analysis documentation, guides, and tech stack PDF reports.", table_cell)
        ]
    ]

    st_table = Table(struct_data, colWidths=[110, 125, 288])
    st_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0F172A")),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")]),
    ]))
    story.append(st_table)
    story.append(Spacer(1, 10))

    # 5. Summary & Technical Takeaways
    story.append(Paragraph("5. Summary & Technical Takeaways", h1_style))
    story.append(Paragraph(
        "TRENVO project me ek complete full-stack AI/Data Science lifecycle successfully execute ki gayi hai:<br/>"
        "1. <b>Data Collection & Cleaning:</b> 114k Spotify data points ko Pandas ke sath reliably clean aur structure kiya gaya.<br/>"
        "2. <b>Domain Feature Engineering:</b> Music industry signals (popularity, energy, danceability, tempo) ko weight dekar `trend_score` formulate kiya gaya.<br/>"
        "3. <b>Supervised Machine Learning:</b> Scikit-Learn ke Random Forest model se trending probability predict ki gayi.<br/>"
        "4. <b>Real-time Cloud Integration:</b> Apple Music aur MusicBrainz REST APIs ke sath live chart synchronization kiya gaya.<br/>"
        "5. <b>Modern UI/UX:</b> Streamlit aur Plotly ke through responsive dark-themed dashboard create kiya gaya jo desktop aur mobile dono par smoothly render hota hai.<br/><br/>"
        "Yeh PDF documentation project presentation, viva, project report, ya portfolio documentation ke liye 100% ready aur structured hai.",
        body_style
    ))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"PDF Successfully generated at: {output_filename}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        out_path = sys.argv[1]
    elif os.path.exists("docs"):
        out_path = os.path.join("docs", "TRENVO_Technology_Stack_Hinglish.pdf")
    else:
        out_path = "TRENVO_Technology_Stack_Hinglish.pdf"
    generate_pdf(out_path)
