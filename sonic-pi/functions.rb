define :ring_delete_at do |ring, index|
    ringClone = ring.drop(0)
    ringClone = ringClone.take(index)+ringClone.drop(index+1)

    return ringClone
end

define :ring_set_at do |ring, index, value|
    ringClone = ring.drop(0)
    ringClone[index] = value

    return ringClone
end
