<template>
  <div class="about">
    <h1>关于</h1>

    <section class="intro">
      <h2>关于我</h2>
      <p>网名算不尽，目前某不知名双非二本数学系大一在读。喜欢技术，方向想往 AI Infra 走，正在努力。</p>
      <p>平时写代码、做实验、踩坑。这个博客主要分享一些折腾过程中的经验心得和个人看法。内容会偏技术向，偶尔也可能聊聊学习方法和工具。</p>
      <p>本人层次不高，不写教程，不讲大道理。只希望我趟过的坑，能帮诸位少走一段弯路。</p>
      <p>欢迎交流，尽量直接。</p>
    </section>

    <section class="contact">
      <h2>联系方式</h2>
      <ul>
        <li><a href="https://github.com/suan2inf" target="_blank" rel="noopener">GitHub</a></li>
        <li><a href="mailto:3662927683@qq.com">Email</a></li>
      </ul>
    </section>

    <section class="site-info">
      <div class="info-card">
        <h3>关于本站</h3>
        <ul>
          <li>自建的个人博客，记录学习和踩坑过程</li>
          <li>前端：Vue 3 + Vite</li>
          <li>后端：FastAPI + SQLAlchemy</li>
          <li>数据库：SQLite</li>
        </ul>
      </div>
    </section>
  </div>
</template>

<style scoped>
.about { max-width: 640px; }

h1 {
  font-size: 28px;
  font-weight: 700;
  color: var(--heading);
  margin-bottom: 36px;
}

.intro {
  margin-bottom: 40px;
}

.intro h2 {
  font-size: 18px;
  font-weight: 600;
  color: var(--heading);
  margin-bottom: 16px;
}

.intro p {
  color: var(--text);
  margin-bottom: 14px;
  line-height: 1.85;
  text-align: justify;
}

.contact {
  margin-bottom: 40px;
}

.contact h2 {
  font-size: 18px;
  font-weight: 600;
  color: var(--heading);
  margin-bottom: 16px;
}

.contact ul {
  list-style: none;
  display: flex;
  gap: 20px;
}

.contact a {
  color: var(--accent);
  font-size: 15px;
  transition: opacity 0.15s;
}

.contact a:hover { opacity: 0.7; }

.site-info {
  border-top: 1px solid var(--border);
  padding-top: 32px;
}

.info-card {
  background: var(--paper-bg);
  border: 1px solid var(--paper-border);
  border-radius: var(--radius);
  padding: 20px 24px;
}

.info-card h3 {
  font-size: 16px;
  font-weight: 600;
  color: var(--heading);
  margin-bottom: 12px;
}

.info-card ul {
  list-style: none;
}

.info-card li {
  padding: 5px 0;
  color: var(--text-secondary);
  font-size: 14px;
}

.info-card li::before {
  content: "— ";
  color: var(--paper-secondary);
}
</style>
