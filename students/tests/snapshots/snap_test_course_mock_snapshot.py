# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['CourseMockSnapshotTestCase::test_get_course_list_with_mock 1'] = [
    {
        'code': 'ITA0043',
        'department': 1,
        'id': 1,
        'name': 'Python Programming'
    },
    {
        'code': 'ITA0044',
        'department': 1,
        'id': 2,
        'name': 'Data Structures'
    }
]

snapshots['CourseMockSnapshotTestCase::test_post_course_with_mock 1'] = {
    'code': 'ITA0050',
    'department': 1,
    'id': 3,
    'name': 'Machine Learning'
}
