import { data } from './data.js';
import { ProjectView } from './ProjectView.js';

let numberOfPanels = 8; // 패널 개수
let panelSize = 300; // 패널 크기(폭)
// 2파이는 360도 => 라디안 값으로 변환
let unitRadian = 2*Math.PI / numberOfPanels;
let unitDegree = 360 / numberOfPanels;
let prevPageYOffset; // 이전 스크롤 위치
let scrollDirection; // 스크롤 방향(위/아래)

let projectView;

let currentIndex; // 현재 활성화된 프로젝트 번호
let currentPanelElem; // 현재 활성화된 패널 요소 객체

let loaderElem;
let panelsElem;
let panelListElem;
let panelItemElems;
let observerElems;
let projectListElem;

function setElems() {
	loaderElem = document.querySelector('.loader-wrapper');
	panelsElem = document.querySelector('.panels');
	panelListElem = document.querySelector('.panel-list');
	panelItemElems = document.querySelectorAll('.panel-item');
	observerElems = document.querySelectorAll('.observer-ready');
	projectListElem = document.querySelector('.project-list');
}

// 각 패널들의 회전과 위치 결정
function setPanelItems() {
	// 패널 폭은 300
	const dist = (panelSize / 2) / Math.tan(unitRadian / 2) + (panelSize * 0.65);
	
	for (let i = 0; i < panelItemElems.length; i++) {
		panelItemElems[i].style.transform = `rotateY(${unitDegree * i}deg) translateZ(${-dist}px)`;
		panelItemElems[i].style.backgroundColor = data[i].color;
	}
}

function inactivatePanel() {
	if (currentPanelElem) {
		currentPanelElem.classList.remove('active');
	}
}

function setCurrentPanel() {
	inactivatePanel();
	currentPanelElem = panelItemElems[currentIndex];
	currentPanelElem.classList.add('active');
}

function rotatePanel() {
	panelListElem.style.transform = `translateZ(${numberOfPanels * 85}px) rotateY(${-unitDegree * currentIndex}deg)`;
	setCurrentPanel();
}

window.addEventListener('load', () => {
	setElems();

	// 이벤트 핸들러 함수로 화살표 함수를 사용하면, this는 addEventListener를 호출한 객체가 "아니다"!
	// loaderElem.addEventListener('transitionend', function () {
	// 	this.remove();
	// 	console.log(this);
	// });
	loaderElem.addEventListener('transitionend', e => {
		e.currentTarget.remove();
		// console.log(e.currentTarget);
	});

	document.body.classList.remove('before-load');

	setPanelItems();

	projectView = new ProjectView();

	// IntersectionObserver
	const io = new IntersectionObserver((entries, observer) => {
		// 눈에 보이기 시작한 객체 isIntersecting : true
		// 완전히 눈에서 사라진 객체 isIntersecting : false
		
		for (let i = 0; i < entries.length; i++) {
			if (entries[i].isIntersecting) {
				// isIntersecting이 true라면

				// 첫번째 프로젝트 처리
				if (entries[i].target.classList.contains('content-observer-start')) {
					currentIndex = 0;
					rotatePanel();
					continue;
				}

				// entries[i].target이 data-project-index값을 가진 요소일 때만 처리
				const projectIndex = entries[i].target.dataset.projectIndex*1;
				if (projectIndex >= 0) {
					if (scrollDirection === 'up') {
						currentIndex = projectIndex + 1;
					} else {
						currentIndex = projectIndex;
					}
					if (currentIndex < numberOfPanels) {
						rotatePanel();
					}
				}

				// 맨 위로 올라갔을 때
				if (
					scrollDirection === 'up' &&
					entries[i].target.classList.contains('header-content')
				)
				{
					panelListElem.style.transform = `translateZ(0) rotateY(0deg)`;
					inactivatePanel();
				}

				// 마지막 프로젝트를 지났을 때
				if (
					scrollDirection === 'down' &&
					entries[i].target.classList.contains('content-observer-end')
				) {
					panelsElem.classList.add('static-position');
				}

				// 마지막 프로젝트에서 올라갈 때
				if (
					scrollDirection === 'up' &&
					currentIndex === numberOfPanels - 1
				) {
					panelsElem.classList.remove('static-position');
				}
			}
		}

		// console.log(scrollDirection);
		console.log(currentIndex);
	});

	observerElems.forEach((item, i) => {
		// console.log(item);
		// console.log(i);
		io.observe(item);
	});

	window.addEventListener('scroll', () => {
		if (prevPageYOffset > window.pageYOffset) {
			scrollDirection = 'up';
		} else {
			scrollDirection = 'down';
		}
		prevPageYOffset = window.pageYOffset;

		// console.log(scrollDirection);
	});

	projectListElem.addEventListener('click', e => {
		// console.log(e.target);
		if (e.target.classList.contains('project-btn')) {
			projectView.show(data[ e.target.dataset.projectIndex ]);
		}
	});

});
