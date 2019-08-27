var booze = new Vue({
    el: '#booze',
    data: {
        images: [],
        lazyload: lazyLoadInstance = new LazyLoad({
            elements_selector: ".lazyload"
        })
    },
    methods: {
        loadImages: function () {
            fetch("/api/v1/pictures")
                .then(res => res.json())
                .then(res => {
                    res.forEach(function(e){
                        const theDate = new Date(e.date);
                        e.formattedDate = theDate.toLocaleTimeString('de-DE',  {hour: '2-digit', minute:'2-digit'});
                    });
                    this.images=res;
                    this.reverse();
                }
                );
        },
        reverse: function () {
            this.images = this.images.reverse();
        },
       
        openImage: function(index) {
            var pswpElement = document.querySelectorAll('.pswp')[0];
            // define options (if needed)
            var options = {
                shareButtons: [
       			{id:'download', label:'Bild speichern', url:'{{raw_image_url}}', download:true}
		        ],
                index: index // start at first slide
            };
            // Initializes and opens PhotoSwipe
            var gallery = new PhotoSwipe( pswpElement, PhotoSwipeUI_Default, this.images, options);
            gallery.init();
        }
    },
    mounted: function () {
        this.loadImages();       
    },
    updated: function(){
        if (this.lazyload){
            this.lazyload.update();
        }
    }
});
