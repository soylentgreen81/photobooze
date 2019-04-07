var booze = new Vue({
    el: '#booze',
    data: {
        images: [],
        imageLimit: 0,
        imageIndex: -1,
    },
    methods: {
        loadImages: function () {
            fetch("/api/v1/pictures")
                .then(res => res.json())
                .then(res => {
                    this.images=res;
                    this.imageLimit = Math.min(this.images.length, 48);
                }
                );
        },
        reverse: function () {
            this.images = this.images.reverse();
        },
        infiniteScroll: function () {
            const scrolling = document.scrollingElement;
            if (scrolling.clientHeight + scrolling.scrollTop >= scrolling.scrollHeight - 100) {
                this.imageLimit = Math.min(this.images.length, this.imageLimit+ 5);
            }
        },
    },
    mounted: function () {
        this.loadImages();
        document.addEventListener("scroll", this.infiniteScroll);
    }
});