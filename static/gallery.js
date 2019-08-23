var booze = new Vue({
    el: '#booze',
    data: {
        images: [],
        imageLimit: 0,
        imageIndex: -1,
        hammertime: null,
        fetchSize: 1000,
    },
    methods: {
        loadImages: function () {
            fetch("/api/v1/pictures")
                .then(res => res.json())
                .then(res => {
                    this.images=res;
                    this.imageLimit = Math.min(this.images.length, this.fetchSize);
                    this.reverse();
                }
                );
        },
        reverse: function () {
            this.images = this.images.reverse();
        },
        infiniteScroll: function () {
            const scrolling = document.scrollingElement;
            if (scrolling.clientHeight + scrolling.scrollTop >= scrolling.scrollHeight - 100) {
                this.imageLimit = Math.min(this.images.length, this.imageLimit+ this.fetchSize);
            }
        },
        openImage: function(index) {
            this.imageIndex = index;
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
        },
        closeImage: function() {
            this.imageIndex = -1;
        },
        nextImage: function(){
            if (this.imageIndex == this.images.length -1)
                this.imageIndex = 0;
             else
                this.imageIndex++;
        },
        previousImage: function(){
            if (this.imageIndex == 0)
                this.imageIndex = this.images.length -1;
            else
                this.imageIndex--;
        },
    },
    mounted: function () {
        this.loadImages();
        document.addEventListener("scroll", this.infiniteScroll);
       
    }
});
