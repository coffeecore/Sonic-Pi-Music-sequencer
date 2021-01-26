define :ring_clone do |ring|
    ringClone = ring.drop(0)

    return ringClone
end

define :ring_delete_at do |ring, index|
    ringClone = ring_clone(ring)
    ringClone = ringClone.take(index)+ringClone.drop(index+1)

    return ringClone
end

define :ring_add_at do |ring, index, value|
    ringClone = ring_clone(ring)
    ringClone[index] = value

    return ringClone
end
