/**
 * 업무 말투 변환기 (BizTalk) — 프론트엔드 비즈니스 로직
 */

document.addEventListener('DOMContentLoaded', () => {
  // DOM 요소 선택
  const targetBtns = document.querySelectorAll('.target-btn');
  const inputText = document.getElementById('inputText');
  const outputText = document.getElementById('outputText');
  const outputPlaceholder = document.getElementById('outputPlaceholder');
  const convertBtn = document.getElementById('convertBtn');
  const copyBtn = document.getElementById('copyBtn');
  const charCount = document.getElementById('charCount');
  const outputCharCount = document.getElementById('outputCharCount');
  const personaBadge = document.getElementById('currentPersonaBadge');
  const toast = document.getElementById('toast');

  // 현재 선택된 대상 (기본값: boss)
  let currentTarget = 'boss';

  const TARGET_LABELS = {
    boss: '상사 / 임원',
    colleague: '타팀 동료',
    client: '고객 / 외부',
    team: '팀 내 동료',
  };

  // 1. 수신 대상 버튼 클릭 이벤트
  targetBtns.forEach((btn) => {
    btn.addEventListener('click', () => {
      targetBtns.forEach((b) => {
        b.classList.remove('active');
        b.setAttribute('aria-selected', 'false');
      });

      btn.classList.add('active');
      btn.setAttribute('aria-selected', 'true');
      currentTarget = btn.dataset.target;

      if (personaBadge) {
        personaBadge.textContent = TARGET_LABELS[currentTarget] || '상사 / 임원';
      }
    });
  });

  // 2. 글자 수 실시간 카운트
  inputText.addEventListener('input', () => {
    const len = inputText.value.length;
    charCount.textContent = `${len}자`;
  });

  // 3. 단축키 지원 (Ctrl + Enter 또는 Cmd + Enter)
  inputText.addEventListener('keydown', (e) => {
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
      e.preventDefault();
      convertTone();
    }
  });

  // 4. 말투 변환 실행 함수
  async function convertTone() {
    const text = inputText.value.trim();

    if (!text) {
      alert('변환할 내용을 1자 이상 입력해 주세요.');
      inputText.focus();
      return;
    }

    setLoading(true);

    try {
      const response = await fetch('/api/convert', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          text: text,
          target_audience: currentTarget,
        }),
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `서버 오류 (HTTP ${response.status})`);
      }

      const data = await response.json();
      const converted = data.converted_text || '';

      // 결과 영역 렌더링
      outputPlaceholder.style.display = 'none';
      outputText.style.display = 'block';
      outputText.value = converted;

      copyBtn.disabled = false;
      outputCharCount.textContent = `${converted.length}자`;

    } catch (err) {
      console.error('말투 변환 실패:', err);
      alert(`변환 중 오류가 발생했습니다: ${err.message}`);
    } finally {
      setLoading(false);
    }
  }

  convertBtn.addEventListener('click', convertTone);

  // 5. 로딩 상태 토글
  function setLoading(isLoading) {
    const btnText = convertBtn.querySelector('.btn-text');

    if (isLoading) {
      convertBtn.classList.add('loading');
      convertBtn.disabled = true;
      if (btnText) btnText.textContent = 'AI 변환 중...';
    } else {
      convertBtn.classList.remove('loading');
      convertBtn.disabled = false;
      if (btnText) btnText.textContent = '말투 변환하기';
    }
  }

  // 6. 결과 복사 기능
  copyBtn.addEventListener('click', async () => {
    const textToCopy = outputText.value;
    if (!textToCopy) return;

    try {
      await navigator.clipboard.writeText(textToCopy);
      showToast('클립보드에 복사되었습니다! 📋');

      // 버튼 시각 피드백
      copyBtn.classList.add('copied');
      const copyTextSpan = copyBtn.querySelector('.copy-text');
      const originalText = copyTextSpan.textContent;
      copyTextSpan.textContent = '복사 완료! ✔';

      setTimeout(() => {
        copyBtn.classList.remove('copied');
        copyTextSpan.textContent = originalText;
      }, 2000);

    } catch (err) {
      console.error('클립보드 복사 실패:', err);
      // fallback: 구형 execCommand 시도
      outputText.select();
      document.execCommand('copy');
      showToast('복사되었습니다!');
    }
  });

  // 7. 토스트 알림 표시
  let toastTimer = null;
  function showToast(message) {
    if (!toast) return;
    toast.textContent = message;
    toast.classList.add('show');

    if (toastTimer) clearTimeout(toastTimer);
    toastTimer = setTimeout(() => {
      toast.classList.remove('show');
    }, 2200);
  }
});
