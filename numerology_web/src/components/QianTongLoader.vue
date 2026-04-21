<script setup lang="ts">
defineProps<{ text?: string }>()
</script>

<template>
  <div class="qt-loader">
    <div class="stage">
      <!-- 手 -->
      <div class="hand">🤚</div>
      <!-- 签桶 -->
      <div class="bucket">
        <div class="sticks">
          <span class="stick s1"></span>
          <span class="stick s2"></span>
          <span class="stick s3"></span>
          <span class="stick s4"></span>
          <span class="stick s5"></span>
        </div>
        <div class="body"></div>
        <div class="rim"></div>
      </div>
    </div>
    <p class="hint">{{ text || '摇 签 中…  天 机 徐 徐 而 来' }}</p>
  </div>
</template>

<style scoped>
.qt-loader {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 26px;
  padding: 40px 0 20px;
}
.stage {
  position: relative;
  width: 160px;
  height: 200px;
  transform-origin: 50% 90%;
  animation: shake 1.2s ease-in-out infinite;
}
.hand {
  position: absolute;
  top: 8px;
  left: 50%;
  transform: translateX(-50%) rotate(8deg);
  font-size: 56px;
  filter: drop-shadow(0 2px 2px rgba(0,0,0,0.15));
}
.bucket {
  position: absolute;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 110px;
  height: 140px;
}
.bucket .body {
  position: absolute;
  left: 4px; right: 4px;
  top: 22px; bottom: 0;
  background: linear-gradient(to bottom, #a8814b 0%, #7a5a2e 100%);
  border: 2px solid #5c3f1c;
  border-radius: 6px 6px 14px 14px;
  box-shadow: inset 0 -6px 0 rgba(0,0,0,0.18), inset 0 2px 0 rgba(255,255,255,0.1);
}
.bucket .body::before,
.bucket .body::after {
  content: '';
  position: absolute;
  left: 0; right: 0;
  height: 3px;
  background: rgba(0,0,0,0.18);
}
.bucket .body::before { top: 22%; }
.bucket .body::after { top: 66%; }
.bucket .rim {
  position: absolute;
  top: 14px; left: 0; right: 0;
  height: 14px;
  background: #8a6334;
  border: 2px solid #5c3f1c;
  border-radius: 6px;
}
.sticks {
  position: absolute;
  left: 0; right: 0;
  top: -8px;
  height: 40px;
  display: flex;
  justify-content: center;
  align-items: flex-end;
  gap: 3px;
}
.stick {
  display: inline-block;
  width: 4px;
  background: linear-gradient(to bottom, #e9d9b5, #c9a86a);
  border: 1px solid #8a6334;
  border-radius: 2px 2px 0 0;
  transform-origin: 50% 100%;
}
.stick.s1 { height: 38px; transform: rotate(-10deg); animation: wiggle1 0.9s ease-in-out infinite; }
.stick.s2 { height: 44px; transform: rotate(-4deg);  animation: wiggle2 1.1s ease-in-out infinite; }
.stick.s3 { height: 48px; transform: rotate(1deg);   animation: wiggle3 1.0s ease-in-out infinite; }
.stick.s4 { height: 42px; transform: rotate(6deg);   animation: wiggle2 0.95s ease-in-out infinite; }
.stick.s5 { height: 36px; transform: rotate(12deg);  animation: wiggle1 1.05s ease-in-out infinite; }

@keyframes shake {
  0%, 100% { transform: rotate(-10deg); }
  25%      { transform: rotate(8deg) translateY(-3px); }
  50%      { transform: rotate(-6deg); }
  75%      { transform: rotate(10deg) translateY(-4px); }
}
@keyframes wiggle1 {
  0%,100% { transform: rotate(-12deg) translateY(0); }
  50%     { transform: rotate(-6deg)  translateY(-2px); }
}
@keyframes wiggle2 {
  0%,100% { transform: rotate(-2deg) translateY(0); }
  50%     { transform: rotate(4deg)  translateY(-3px); }
}
@keyframes wiggle3 {
  0%,100% { transform: rotate(3deg)  translateY(0); }
  50%     { transform: rotate(-3deg) translateY(-2px); }
}

.hint {
  margin: 0;
  color: var(--ink-soft);
  font-family: var(--font-hand);
  letter-spacing: 0.3em;
  font-size: 15px;
}
</style>
