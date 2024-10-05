<script>
    const courseTitles = document.querySelectorAll('.course-title');

    courseTitles.forEach(title => {
        title.addEventListener('click', () => {
            const content = title.nextElementSibling;
            content.style.display = content.style.display === 'block' ? 'none' : 'block';
            title.querySelector('i').classList.toggle('fa-chevron-down');
            title.querySelector('i').classList.toggle('fa-chevron-up');
        });
    });
</script>
