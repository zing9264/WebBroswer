class MainConsoleScreen {

    constructor(containerElement) {
        this.containerElement = containerElement;
        var numOfchoice=0;
        this.stage=-1;

        this.hide = this.hide.bind(this);
        this.show = this.show.bind(this);
        this._getStart=this._getStart.bind(this);

        this.menuTitleElement = containerElement.querySelector('#choices');

        for (var _ of FLASHCARD_DECKS) {
            this.choiceElement = this._createMenuChoicesDOM(_.title ,numOfchoice);
            this.menuTitleElement.append(this.choiceElement);
            numOfchoice++;
        }

        var choosen = document.querySelectorAll('#choices div');

        for (var i = 0; i < FLASHCARD_DECKS.length; i++) {
            console.log(i.valueOf());
            choosen[i].addEventListener('pointerup', this._getStart);
        }

    }

    show() {
        this.containerElement.classList.remove('inactive');
    }

    hide() {
        this.containerElement.classList.add('inactive');

    }

    _createMenuChoicesDOM(FLASHCARD_DECKNAME,numOfchoice) {
        const menuTitle = document.createElement('div');
        menuTitle.classList.add(numOfchoice);
        menuTitle.textContent = FLASHCARD_DECKNAME;
        return menuTitle;
    }

    _getStart(event) {
        this.hide();
        this.stage=event.currentTarget.classList[0];
        console.log(event);
        console.log(this.stage);
        let Start = new CustomEvent('Start');
        document.dispatchEvent(Start);

    }

    getStage(){
        return this.stage;
    }
}
