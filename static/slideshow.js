var slides = new Vue({
    el: '.slideshow',
    data: {
        images: [],
        slideshow: null
    },
    methods: {
        loadImages: function () {
            fetch("/api/v1/pictures")
                .then(res => res.json())
                .then(res => {
                    this.images=this.shuffle(res);
                    
                }
            );
        },
        shuffle: function shuffle(array) {
            let currentIndex = array.length, temporaryValue, randomIndex;
            
            // While there remain elements to shuffle...
            while (0 !== currentIndex) {
            
                // Pick a remaining element...
                randomIndex = Math.floor(Math.random() * currentIndex);
                currentIndex -= 1;
            
                // And swap it with the current element.
                temporaryValue = array[currentIndex];
                array[currentIndex] = array[randomIndex];
                array[randomIndex] = temporaryValue;
            }
            return array;
        }
       
    },
    mounted: function () {
        this.loadImages();
    },
    updated: function(){
        console.log("update!");
        
        if (this.slideshow == null){
            this.slideshow =  new KenBurnsSlideshow({
                el: document.querySelector('.slideshow')
            });
            console.log("start slideshow");
            this.slideshow.init();    
        }
        else{
            //Hacky hacky!
            this.slideshow.stop();
            this.slideshow.state.slideVisibleEl.classList.remove(this.slideshow.props.cssPrefix + '--has-kenBurnsFx');
            this.slideshow.init();
            
        }
    }
});
