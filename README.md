![Netflix Background](./Tableau/Netflix.jpg)  
# 🎬 Netflix Movies and TV Shows – Data Visualization with Tableau
This project delivers a professional **data analysis and visualization of Netflix Movies & TV Shows** using Tableau.  
As streaming platforms compete fiercely worldwide, this analysis provides actionable insights into **content growth, genre shifts, audience targeting, and market competition**.  
By combining Tableau with **Design Thinking**, we highlight both descriptive analytics (what has happened) and strategic implications (what Netflix should do).
---
## 🌍 Background: Netflix and the Streaming War

Founded in 1997 as a DVD rental service, Netflix has grown into the **world’s largest streaming platform** with 240M+ subscribers in 190+ countries. Its success is fueled by:  

- **Global Expansion** 🌐 – Aggressive scaling post-2015 with localized content.  
- **Original Productions** 🎬 – Heavy investment in Netflix Originals since 2013.  
- **Competition** ⚔️ – Disney+, Amazon Prime, Apple TV+ are catching up.  
- **Personalization** 🤖 – Advanced recommendation system enhancing user experience.  

<p align="center">
  <img src="./Tableau/Netflix-worldwide.jpg" alt="Netflix Worldwide" width="500"/>
</p>

### 🚀 Key Drivers of Netflix’s Growth
- **Innovation & Flexibility**: Rapid product iteration challenged the belief that ads or heavy promotions are the only way to boost views.  
- **Technology**: AI-driven recommendations personalize experiences, keeping engagement high.  
- **Content Strategy**: Massive investment in originals (“By Netflix”) earned global recognition — Oscars, Emmys, BAFTA, Golden Globes, and even Grammys.  


<p align="center">
  <img src="./Tableau/Netflix%20and%20other%20web.jpg" alt="Netflix vs Competitors" width="500"/>
</p>


### ⚔️ Facing the Competition
- **Disney+** 🏰 – 234M+ subs with Marvel, Pixar, Star Wars, Hulu.  
  → But Netflix’s ARPU (11.76 USD) is nearly double Disney+ (5.95 USD).  
- **Apple TV+** 🍏 – ~25M paid subs; strong premium shows like *The Morning Show* but smaller library (~80 vs Netflix’s 5000+).  
- **Amazon Prime Video** 📦 – ~190M subs; strong originals (*Fleabag*, *Marvelous Mrs. Maisel*) but mixed reputation due to user-generated content.  
- **Other Players**: YouTube TV, Paramount+, HBO Max, Sling — each carving niche segments.  


### 🎯 Netflix’s Marketing Shift
Marketing spend rose from **$2.2B (2020) → $2.5B (2022)**.  
- Old Strategy: Build broad **brand awareness**.  
- New Strategy: Spotlight **individual shows & movies**, delivering unique experiences that strengthen customer loyalty.  

### User Segmentation

<img src="./Tableau/User Netflix.jpg" width="600"/>

- **Teens (13–24)** prefer Anime, Action, Sci-Fi.  
- **Adults (25–44)** watch Drama, Documentaries.  
- **Families (45+)** lean on International Movies and Comedies.  
- **Key insight:** Personalized recommendations must vary **by age & culture**.  

---

## 🔄 Netflix Strategic Flow & Design Thinking

###  A Fun Approach to Data Analysis
![Netflix Flowchart](./Tableau/Netflix%20Flowchart.png)
Ever wondered if you should watch Netflix? This fun flowchart gives us a great way to think about our data analysis process.
Just like the chart helps you decide, our project follows a similar logical flow:
1.  **Start:** We gather all the raw data, focusing on **content supply** from different countries and genres.
2.  **Process:** We then analyze user engagement by looking at **ratings and user segmentation** to see what people are really watching.
3.  **End:** Finally, we use these findings to generate **strategic insights** that can help Netflix stay competitive and keep viewers engaged. 

### Applying Design Thinking
![Design Thinking](./Tableau/Design%20Thinking.png)

1. **Empathize** – Identify user needs (local content, genre preference).  
2. **Define** – Spot challenges (e.g., limited family content vs Disney+).  
3. **Ideate** – Propose ideas (regional co-productions, niche genres).  
4. **Prototype** – Create dashboards & simulate content strategies.  
5. **Test** – Measure success with engagement & retention metrics.  

---

## 📊 Domain Insights and Visualizations

### 1. Content Growth Over Time
<p align="center">
  <img src="./Tableau/Content%20by%20years.png" alt="Content by years" width="800"/>
</p>

- Netflix’s catalog **expanded sharply after 2015**, with a peak roughly between **2018–2020**.  
- Post-2020 the growth curve **flattens** and shows signs of stabilization.  
- The initial surge aligns with Netflix’s aggressive international market entry and Originals production.

**🔑 Key Insight:**  
The flattening after 2020 signals a strategic pivot from sheer volume → **curated, higher-value originals**. Prioritize measuring ROI per title (cost vs engagement) and shift budget to high-LTV content.

### 2. Top 10 Content-Producing Countries
<p align="center">
  <img src="./Tableau/Top%2010%20producing%20countries.png" alt="Top 10 producing countries" width="700"/>
</p>

- **USA** leads by a large margin; **India, UK, Canada** follow.  
- Emerging producers: **South Korea, Japan, France** (rising rapidly).  
- Country mix differs by type: some countries skew toward TV shows, others toward movies.

**🔑 Key Insight:**  
Netflix’s **local-for-global** strategy is working — invest selectively in regional production hubs (e.g., K-content, Indian TV) that produce exportable hits. Use country-level economics (production cost vs global viewership) to prioritize investments.


### 3. Trend in Publishing Genres Over Years
<p align="center">
  <img src="./Tableau/Trend%20in%20publishing%20over%20years.png" alt="Trend in publishing over years" width="800"/>
</p>

- Core genres: **Drama, Comedy, International Movies**.  
- Notable growth in **Anime, Docuseries, Reality** segments since ~2017.  
- Genre mix shifted from homogeneous (pre-2015) → diversified (post-2015).

**🔑 Key Insight:**  
Genre diversification reduces churn by serving both mass and niche audiences (long-tail value). Prioritize personalized surfacing of niche genres to increase engagement among segmented audiences.


### 4. Age-Rating Category Correlations (Genre × Rating)
<p align="center">
  <img src="./Tableau/Age%20rating%20category%20correlations.png" alt="Age rating category correlations" width="800"/>
</p>

- Strong links: **TV-MA ↔ International Movies**, **TV-14 ↔ International TV Shows**, **R ↔ Dramas**.  
- Mature ratings are heavily represented across international genres.

**🔑 Key Insight:**  
Netflix aligns rating strategy with genre & region to maximize relevance. This supports highly targeted recommendation rules (e.g., promote TV-MA international titles to cohorts that historically engage with mature international drama).


### 5. Number of Content by Rating
<p align="center">
  <img src="./Tableau/Number%20of%20Content%20followed%20by%20rating.png" alt="Number of content by rating" width="600"/>
</p>

- **TV-MA and TV-14** constitute the largest share of titles.  
- **Family / G / TV-Y** content is under-represented relative to the adult catalog.

**🔑 Key Insight:**  
Netflix’s portfolio skews mature — great for young-adult retention but leaves a **family-segment gap** where competitors (Disney+) outperform. Consider targeted family content acquisition to diversify ARPU sources and household reach.


### 6. Distribution of Content by Country (detailed)
<p align="center">
  <img src="./Tableau/Distribution%20of%20content%20followed%20by%20countries.png" alt="Distribution by country" width="800"/>
</p>

- Country distribution shows concentration in a few hubs but increasing tail of smaller producing countries.  
- Some countries produce more TV formats; others focus on films.

**🔑 Key Insight:**  
Leverage smaller-country content as **cost-effective experimentation** (lower production cost, potential viral global hits). Build a fast A/B pipeline to test and scale region-originated formats with global appeal.


### 7. Cast Distribution (cast-size / cast-diversity by genre)
<p align="center">
  <img src="./Tableau/Distribution%20cast%20with%20different%20listed%20in.png" alt="Distribution cast with different listed in" width="800"/>
</p>

- Genres like **Drama, International Movies, Comedies** have larger casts and higher cast-diversity.  
- Larger ensembles correlate with longer runtimes / multi-episode formats.

**🔑 Key Insight:**  
Investing in ensemble, star-driven productions increases discoverability across markets. Use cast-network analytics to identify cross-market actor clusters for co-productions and targeted promotion.


### 8. Number of Rating's Content by Year (Temporal evolution)
<p align="center">
  <img src="./Tableau/Number%20of%20rating%27s%20content%20years.png" alt="Number of rating's content years" width="800"/>
</p>

- **TV-MA & TV-14** show rapid growth since 2010 with acceleration during global expansion.  
- **G/PG** content remains relatively flat over the same period.

**🔑 Key Insight:**  
Temporal patterns confirm a deliberate tilt toward maturity-focused storytelling. For long-term resilience, combine this focus with selective family-oriented investments to keep multi-generational households engaged.

---

## 📊 Final Integrated Dashboard

<img src="./Tableau/Dashboard.png" width="900"/>

- Interactive filters for ratings, genres, and regions.  
- Unified storytelling: Content growth ➝ Ratings ➝ Countries ➝ Segmentation.  
- Built for both **analytical exploration** and **executive reporting**.  

---

## 📈 Executive Insights  
- Netflix dominates **mature-rated global content**, but weak in **family-friendly space** where Disney+ excels.  
- **Regional hubs** (India, Korea, Japan) drive growth, proving the success of the **“local-for-global” model**.  
- Content strategy has shifted **from volume (2015–2020) → curation & Originals (post-2020)**.  
- **Personalization & niche genres** (anime, docuseries) are critical for user retention.  
- **Star-driven productions** enhance cross-market appeal and strengthen Netflix’s global brand.  


## 📊 Executive Takeaways  
① **Strategic pivot confirmed**: Focus on curated Originals with strong ROI and retention, not sheer volume.  
② **Local-for-global works**: Scale investments in regional co-productions and expand global distribution of local hits.  
③ **Audience concentration risk**: Mature-content dominance retains young adults but leaves the **family segment untapped**.  
④ **Long-tail genres = stickiness**: Enhance recommendation algorithms to push anime, docuseries, and other niche content.  
⑤ **Talent economics matter**: Use cast-network insights to guide content planning, marketing, and partnerships.  


## ✅ Recommended Next Steps  
- **Short-term (0–6M):**  
  - Deploy **title-level ROI dashboards** (cost, first-28-day views, retention lift).  
  - Improve personalization for niche genres to increase long-tail watch time.  

- **Mid-term (6–12M):**  
  - Pilot **family-content acquisition program** in US + India; measure household penetration impact.  
  - Establish **cast-network KPIs** to inform co-production and talent contracting.  

- **Long-term (12M+):**  
  - Scale successful family and regional strategies globally.  
  - Continuously refine **data-driven segmentation** for retention and ARPU optimization. 
---
# 🛠️ Methodology & Data Transparency  

- **Data Source**: Kaggle’s *Netflix Movies and TV Shows* dataset (~8,800 titles, up to 2021), originally compiled from Flixable + Netflix public catalog.  
- **Preprocessing Steps**:  
  - Cleaned missing values in `country`, `cast`, and `date_added`.  
  - Standardized `genre` and merged sub-categories (e.g., “Intl. Movies” vs “International Movies”).  
  - Split dataset into **Movies vs TV Shows** for separate analysis.  
- **Limitations**:  
  - Dataset ends at 2021 → excludes recent Netflix Originals.  
  - Some metadata (e.g., viewership, budget, churn impact) is not public.  
  - Genre overlap (multi-tagged shows) may slightly inflate counts.  

> ⚖️ Including methodology + limitations improves research transparency and aligns with **academic best practice**.  

---

# 🌍 Comparative Benchmarking  

Netflix’s growth is clearer when placed in **industry context**:  

- **Disney+** → *Family-first positioning*. Strong catalog of Marvel, Pixar, and Star Wars makes Disney+ the clear winner in **G/PG-rated content**.  
- **Amazon Prime Video** → Broad distribution (bundled with Prime), but relatively *low engagement per title*.  
- **Apple TV+** → Fewer titles, but *high ROI per show* (e.g., Ted Lasso, The Morning Show) with strong awards presence.  

> 📌 Netflix dominates **global mature-rated content**, but competitors highlight gaps in **family appeal** (Disney+), **distribution bundling** (Amazon), and **prestige-per-title strategy** (Apple TV+).  

---

# 🔮 Future Opportunities for Netflix  

To sustain leadership, Netflix should look beyond descriptive growth into **strategic foresight**:  

1. **AI-Driven Content Creation**  
   - Generative AI for **script ideation**, **subtitle localization**, and **personalized trailers**.  
   - Reduces production cost + accelerates global releases.  

2. **Gamification & Interactive Content**  
   - Expand *Bandersnatch-style* interactive shows.  
   - Drives **engagement, rewatchability**, and differentiates from rivals.  

3. **Partnership Ecosystem**  
   - Collaborate with **telecom operators** (e.g., bundle Netflix with 5G data plans).  
   - Boosts ARPU + strengthens market penetration in emerging economies.  

4. **Sustainability & ESG Branding**  
   - Invest in **carbon-neutral productions** and green studios.  
   - Enhances brand equity, attracts ESG-focused investors, and improves compliance in EU markets.  

> 🚀 These moves can **future-proof Netflix** while balancing brand identity (*“edgy, global, personalized”*) with **untapped growth pockets** (family, interactive, ESG).  

---
## 👨‍💻 Author

- **Author**: [TheHien04](https://github.com/TheHien04)  
- **Role**: Data Analyst | Tableau Developer  
- **Dataset**: Kaggle — Netflix Movies and TV Shows (~8.8K entries) [Kaggle Netflix Titles](https://www.kaggle.com/shivamb/netflix-shows)  
- **License**: Academic & educational purposes  
- **Tools**: Tableau, Python (Pandas), SQL

  
