function scrollToProjectView() {
    // 해당 프로젝트로 스크롤 이동
    const projectElement = document.querySelector('#emotion3');
    const scrollContent = document.querySelector('.scroll-content');
    const scrollPosition = projectElement.offsetTop - scrollContent.offsetTop;
    scrollContent.scrollTo({ top: scrollPosition, behavior: 'smooth' });
}