export class ProjectView {
	constructor() {
		this.bodyElem = document.createElement('div');
		this.bodyElem.classList.add('cover-panel');
		document.body.appendChild(this.bodyElem);

		this.bodyElem.addEventListener('click', e => {
			if (e.target.classList.contains('back-btn')) {
				this.hide();
			}
		});
	}

	show(data) {
		document.body.classList.add('scroll-lock');
		this.bodyElem.style.backgroundColor = data.color;

		this.bodyElem.innerHTML = `
			<section class="project-view">
				<button class="back-btn"><span></span></button>
				<header class="project-view-header">
					<div class="width-setter">
						<h1 class="project-view-title">${data.title}</h1>
					</div>
				</header>
				<div class="project-view-content width-setter">
					<figure class="a11y-hidden-bg project-view-image" style="background-image: url(${data.image});">
						<img class="a11y-hidden" src="${data.image}" alt="${data.title}">
					</figure>
					<div class="project-view-desc width-setter">
						${data.description}
					</div>
				</div>
			</section>
		`;

		const timerId = setTimeout(() => {
			this.bodyElem.classList.add('active');
			clearTimeout(timerId);
		}, 100);
	}

	hide() {
		document.body.classList.remove('scroll-lock');
		this.bodyElem.classList.add('close');

		const timerId = setTimeout(() => {
			this.bodyElem.classList.remove('active', 'close');
			clearTimeout(timerId);
		}, 1000);
	}
}