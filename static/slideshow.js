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
                    this.images=res;
                    
                }
            );
        },
       
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
            const currentSlide = this.slideshow.state.slideVisibleNum;
            console.log(`stopped at ${currentSlide}`);
            this.slideshow.state.slideVisibleEl.classList.remove(this.slideshow.props.cssPrefix + '--has-kenBurnsFx');
            this.slideshow.init();
            this.slideshow.state.slideVisibleNum = currentSlide;
        }
    }
});
