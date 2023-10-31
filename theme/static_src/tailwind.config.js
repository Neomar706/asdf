module.exports = {
    content: [
        '../templates/**/*.html',
        '../../templates/**/*.html',
        '../../**/templates/**/*.html',
    ],
    darkMode: 'class',
    theme: {
        extend: {
            spacing: {
                'content': 'calc(100vh - 3.5rem)'
            },
            colors: {
                cgray: {
                    600: '#3D3D3D',
                    700: '#272727',
                    800: '#222222',
                    900: '#0F0F0F',
                }
            }
        },
    },
    plugins: [
        require('@tailwindcss/forms'),
        require('@tailwindcss/typography'),
        require('@tailwindcss/line-clamp'),
        require('@tailwindcss/aspect-ratio'),
        // require('tailwind-scrollbar')
    ],
}
