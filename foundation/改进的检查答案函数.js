// 改进的检查答案函数
async function checkAnswers() {
    await loadStandardAnswers();
    
    let totalAnswerableQuestions = 0;
    let correctCount = 0;
    let incorrectInputs = [];
    
    document.querySelectorAll('.answer-input').forEach(input => {
        const ref = input.dataset.reference;
        const hasAnswer = input.dataset.hasAnswer === 'true';
        
        if (!ref || !hasAnswer) {
            return;
        }
        
        const questionId = input.dataset.question;
        const answerKey = `q${questionId}_${ref}`;
        const answerInfo = standardAnswers[answerKey];
        
        if (!answerInfo || !answerInfo.has_data) {
            return;
        }
        
        totalAnswerableQuestions++;
        
        const userAnswer = input.value.trim();
        const standardAnswer = answerInfo.text || '';
        
        // 清除之前的标记
        input.classList.remove('correct', 'incorrect', 'partial');
        
        const feedbackDiv = input.parentElement.querySelector('.answer-feedback');
        
        if (userAnswer === '') {
            // 空答案 - 标记为错误
            input.classList.add('incorrect');
            feedbackDiv.textContent = '✗ 请填写答案';
            feedbackDiv.className = 'answer-feedback incorrect show';
            incorrectInputs.push(input);
        } else {
            // 相似度检查
            const similarity = calculateSimilarity(userAnswer, standardAnswer);
            
            if (similarity >= 0.85) {
                input.classList.add('correct');
                feedbackDiv.textContent = '✓ 正确！';
                feedbackDiv.className = 'answer-feedback correct show';
                correctCount++;
            } else if (similarity >= 0.6) {
                input.classList.add('partial');
                feedbackDiv.textContent = '△ 部分正确，请对照标准答案修改';
                feedbackDiv.className = 'answer-feedback partial show';
                incorrectInputs.push(input);
            } else {
                input.classList.add('incorrect');
                feedbackDiv.textContent = '✗ 不正确，请对照标准答案修改';
                feedbackDiv.className = 'answer-feedback incorrect show';
                incorrectInputs.push(input);
            }
        }
    });
    
    // 如果有错误的答案，定位到第一个错误位置
    if (incorrectInputs.length > 0) {
        const firstIncorrect = incorrectInputs[0];
        // 平滑滚动到第一个错误位置
        firstIncorrect.scrollIntoView({ 
            behavior: 'smooth', 
            block: 'center' 
        });
        // 短暂聚焦到第一个错误输入框
        setTimeout(() => {
            firstIncorrect.focus();
        }, 500);
        
        showToast(`❌ 发现 ${incorrectInputs.length} 个错误，已定位到第一个错误`);
    } else if (correctCount === totalAnswerableQuestions && totalAnswerableQuestions > 0) {
        showToast('🎉 所有答案都正确！');
    } else if (totalAnswerableQuestions === 0) {
        showToast('ℹ️ 本节没有可检查的题目');
    } else {
        showToast(`✓ 检查完成 - ${correctCount}/${totalAnswerableQuestions} 正确`);
    }
}