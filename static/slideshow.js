var slides = new Vue({
    el: '.slideshow',
    data: {
        images: [],
        slideshow: null,
        timer: null
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
            while (0 !== currentIndex) {
                randomIndex = Math.floor(Math.random() * currentIndex);
                currentIndex -= 1;
                temporaryValue = array[currentIndex];
                array[currentIndex] = array[randomIndex];
                array[randomIndex] = temporaryValue;
            }
            return array;
        }
       
    },
    mounted: function () {
        this.timer = setInterval(this.loadImages, 1000*60*5); 
        this.loadImages();
    },
    beforeDestroy: function(){
        clearInterval(this.timer);
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
