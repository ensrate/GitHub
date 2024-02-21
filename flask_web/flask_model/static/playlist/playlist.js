// <script type="module" src="./assets/main.js"></script> --> 이걸 먼저 html에 삽입해야함
import { data } from './data.js';
import { ProjectView } from './ProjectView.js';

let numberOfPanels = 7; // 패널 개수
let panelSize = 400; // 패널 크기(폭)
let unitRadian = 2 * Math.PI / numberOfPanels;  // radian 표기법 (호도법)  1pi = 180˚, 2pi = 360˚
let unitDegree = 360 / numberOfPanels;  // degree 표기법 (각도법)
let prevPageYOffset; // 이전 스크롤 위치
let scrollDirection; // 스크롤 방향(위/아래)

let projectView;

let currentIndex; // 현재 활성화된 프로젝트 번호
let currentPanelElem; // 현재 활성화된 패널 요소 객체

// setElems 바깥에 변수설정을 해야 DOM객체에 접근할 수 있다
let loaderElem;
let panelsElem;
let panelListElem;
let panelItemElems;
let observerElems;
let projectListElem;

// setElems라는 함수를 이용해 js에서 접근할 DOM객체들을 미리 설정해놓기
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
	const dist = (panelSize * 0.5) / Math.tan(unitRadian * 0.5) + (panelSize * 0.65);
	
	for (let i = 0; i < panelItemElems.length; i++) {
		panelItemElems[i].style.transform = `rotateY(${unitDegree * i}deg) translateZ(${-dist}px)`;
		panelItemElems[i].style.backgroundColor = data[i].color;  // js에선 css와 다르게 카멜표기법을 사용 (background-color x)
	}
}

function inactivatePanel() {
	if (currentPanelElem) {
		currentPanelElem.classList.remove('active');  // 메서드 실행 시 해당 elem에 클래스를 제거(remove)
	}
}

function setCurrentPanel() {
	inactivatePanel();
	currentPanelElem = panelItemElems[currentIndex];
	currentPanelElem.classList.add('active');  // 메서드 실행 시 해당 elem에 클래스를 추가(add)
}

function rotatePanel() {
	panelListElem.style.transform = `translateZ(${numberOfPanels * 85}px) rotateY(${-unitDegree * currentIndex}deg)`;
	setCurrentPanel();
}

window.addEventListener('load', () => {
	setElems(); // 먼저 DOM객체를 내가 정한 변수에 할당하는 함수를 실행시켜야 함

	// 이벤트 핸들러 함수로 화살표 함수를 사용하면, this는 addEventListener를 호출한 객체가 "아니다"!
	// loaderElem.addEventListener('transitionend', function () {
	// 	this.remove(); <=> e.currentTarget.remove(); in 화살표 함수
	// 	console.log(this);
	// });

	// loadwrapper를 2초 동안 보여주고 사라지게 만듭니다.
	loaderElem.style.transition = 'opacity 1s'; // 페이드 인/아웃 효과를 주기 위한 설정
	loaderElem.style.opacity = '1'; // 처음에는 보이도록 설정

	setTimeout(() => {
		loaderElem.style.opacity = '0'; // 2초 후에 loadwrapper의 투명도를 0으로 설정하여 페이드 아웃
		setTimeout(() => {
		loaderElem.remove(); // 1초 후에 loadwrapper 요소를 제거
		}, 1000); // 페이드 아웃 시간과 동일한 값으로 설정
	}, 1000); // 로딩효과 시간설정
		

	// load-wrapper의 transition이 end된 시점을 잡아내서 load-wrapper를 삭제하는 이벤트
	loaderElem.addEventListener('transitionend', e => {  // 매개변수가 1개일 땐 (e) 말고 e로 괄호 생략 가능
		e.currentTarget.remove();
		// console.log(e.currentTarget);
	});

	document.body.classList.remove('before-load');  // body에 붙여놓은 before-load 클래스를 제거하면서 로딩화면이 사라지게 만들기

	setPanelItems();

	projectView = new ProjectView();

	// IntersectionObserver : 현재 보여지는 화면이 어떤건지를 캐치하는 API, entries는
	const io = new IntersectionObserver((entries, observer) => {
		// 눈에 보이기 시작한 객체 isIntersecting : true
		// 완전히 눈에서 사라진 객체 isIntersecting : false
		
		for (let i = 0; i < entries.length; i++) {
			if (entries[i].isIntersecting) {
				// isIntersecting이 true라면  <=>  옵저버가 해당 요소를 현재 보고있는 중이라면

				// 첫번째 프로젝트 처리
				if (entries[i].target.classList.contains('content-observer-start')) {  // class중 'content-observer-start'가 있다면
					currentIndex = 0;
					rotatePanel();
					continue;  // 첫 div의 idx를 0으로 설정했다면 밑의 연산을 하지않고 바로 다음 entry로 넘어가도록하는 장치 (NaN 오류방지)
				}

				// entries[i].target이 data-project-index값을 가진 요소일 때만 처리
				const projectIndex = entries[i].target.dataset.projectIndex * 1;  // str을 int로 바꾸는 방법 : 1을 곱해주기
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

	observerElems.forEach((item, i) => {  // for문과 비슷한 역할을 하는 신기술 (item: DOM요소, i: 인덱스)
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
