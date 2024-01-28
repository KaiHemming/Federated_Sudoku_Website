// https://vitest.dev/guide/
// https://test-utils.vuejs.org/installation/
// https://testdriven.io/blog/vue-unit-testing/

import { describe, it, expect} from 'vitest'
import { shallowMount } from '@vue/test-utils'
import NavBar from '../NavBar.vue'

describe('NavBar.vue Implementation Tests', () => {
    let wrapper = null

    beforeEach(() => {
        wrapper = shallowMount(NavBar);
    })

    afterEach(() => {

    })
})